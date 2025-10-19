from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn
from Libraries.Utilities.PathExtractor import PathExtractor
from Libraries.Keywords.BrowserScripting import BrowserScripting
from robot.api import logger
import json


@library(doc_format = 'ROBOT')
class WorkflowDisplay:
    """
    Class to display and manage a multi-stage workflow progress bar in the browser.
    Supports a two-level hierarchy of Stages and Steps.
    """

    def __init__(self):
        self.builtin = BuiltIn()
        BuiltIn().import_library('Browser')
        self.browser = BuiltIn().get_library_instance('Browser')
        self.workflow_id = "workflow-display-container"
        self.direction = 'ltr'
        self.path_extractor = PathExtractor()
        self.browserScripting = BrowserScripting()

        # New data structures for stages
        self.stages_data = [ ]
        self.step_lookup = { }  # For quick lookup of a step's location
        self.current_active_step = None # To store the name of the currently active step

    @keyword
    def initialize_workflow_display(self, stages_data: list, test_name: str = "Test", direction: str = 'ltr'):
        """Initializes the workflow display with stages and their steps.

        Args:
            stages_data (list): A list of dictionaries, where each dictionary represents a stage.
                                Each dict should have a 'stage' key (str) and a 'steps' key (list of str).
                                Example: `[{'stage': 'Stage 1', 'steps': ['Step A', 'Step B']}]`
            test_name (str): The name of the overall test or workflow.
            direction (str): The display direction, 'ltr' or 'rtl'.
        """
        self.direction = direction.lower()
        self.current_active_step = None # Reset active step on re-initialization

        # For RTL, reverse the stages data to match the visual flow
        if self.direction == 'rtl':
            self.stages_data = list(reversed(stages_data))
        else:
            self.stages_data = stages_data

        self._build_step_lookup()

        self._inject_workflow_css()
        self._create_workflow_html(test_name)
        self._adjust_page_layout()
        logger.info(
            f"Staged workflow display initialized with {len(self.stages_data)} stages in {direction} direction.")

    def _build_step_lookup(self):
        """Creates a lookup map for finding steps quickly."""
        self.step_lookup = { }
        for i, stage in enumerate(self.stages_data):
            for j, step_name in enumerate(stage.get('steps', [ ])):
                if step_name in self.step_lookup:
                    logger.warn(f"Duplicate step name '{step_name}' found. The workflow may not behave as expected.")
                self.step_lookup[ step_name ] = { 'stage_index': i, 'step_index': j }

    @keyword
    def start_workflow_step(self, step_name: str):
        """Marks a workflow step as current/in progress and updates its stage.
        Sets the provided step as the currently active step.
        Automatically completes the previously active step if one exists.
        """
        # If there's a currently active step, complete it first
        if self.current_active_step and self.current_active_step != step_name:
            logger.info(f"Automatically completing previous step: '{self.current_active_step}'")
            self._update_step_and_stage_status(self.current_active_step, "completed")

        self._update_step_and_stage_status(step_name, "current")
        self.current_active_step = step_name  # Set the new current active step

    @keyword
    def complete_workflow_step(self, step_name: str):
        """Marks a workflow step as completed and updates its stage."""
        self._update_step_and_stage_status(step_name, "completed")
        if self.current_active_step == step_name: # Clear active step if it's the one being completed
            self.current_active_step = None

    @keyword(name = "Complete Current Workflow Step")
    def complete_current_workflow_step(self):
        """Marks the currently active workflow step as completed.

        Raises:
            RuntimeError: If no step is currently active.
        """
        if self.current_active_step:
            self.complete_workflow_step(self.current_active_step)
        else:
            raise RuntimeError("No current workflow step defined. Use 'Start Workflow Step' first.")


    @keyword
    def fail_workflow_step(self, step_name: str):
        """Marks a workflow step as failed and updates its stage."""
        self._update_step_and_stage_status(step_name, "failed")
        if self.current_active_step == step_name: # Clear active step if it's the one being failed
            self.current_active_step = None

    @keyword(name = "Fail Current Workflow Step")
    def fail_current_workflow_step(self):
        """Marks the currently active workflow step as failed.

        Raises:
            RuntimeError: If no step is currently active.
        """
        if self.current_active_step:
            self.fail_workflow_step(self.current_active_step)
        else:
            raise RuntimeError("No current workflow step defined. Use 'Start Workflow Step' first.")


    def _update_step_and_stage_status(self, step_name: str, status: str):
        """A single method to find a step, and update its status and its parent stage."""
        if step_name not in self.step_lookup:
            logger.warn(f"Step '{step_name}' not found in workflow definition.")
            return

        lookup_info = self.step_lookup[ step_name ]
        stage_index = lookup_info[ 'stage_index' ]
        step_index = lookup_info[ 'step_index' ]

        self._update_visuals(stage_index, step_index, status)
        logger.info(f"Step '{step_name}' marked as {status}.")

    @keyword
    def remove_workflow_display(self):
        """Removes the workflow display from the browser."""
        remove_script = f"""
        const element = document.getElementById('{self.workflow_id}');
        if (element) element.remove();
        document.body.style.paddingTop = '';
        """
        self.browserScripting.run_js_script(script_string = remove_script, args = None)
        logger.info("Workflow display removed")
        self.current_active_step = None # Clear active step on removal

    def _inject_workflow_css(self):
        """Injects CSS for the staged workflow display."""
        css = f"""
        #workflow-display-container {{
            position: fixed; top: 0; left: 0; width: 100%;
            background: #f8f9fa; border-bottom: 1px solid #dee2e6;
            padding: 8px 15px; /* Slightly reduced padding */
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            z-index: 10000; font-family: 'Segoe UI', sans-serif; box-sizing: border-box;
            display: flex; flex-direction: column; align-items: center;
        }}
        #workflow-display-container.rtl {{
            direction: rtl;
        }}
        .workflow-main-title {{ font-weight: 600; font-size: 13px; /* Slightly smaller font */ margin-bottom: 8px; /* Reduced margin */ color: #212529; }}
        .workflow-stages-wrapper {{
            display: flex;
            align-items: stretch; /* This is key to make all items (stages) the same height */
            justify-content: center;
            gap: 10px; /* Reduced gap */
            width: 100%;
            flex-wrap: wrap; /* Allow wrapping of stages */
            /* For RTL, reverse the flex direction to show stages right-to-left */
            flex-direction: {'row-reverse' if self.direction == 'rtl' else 'row'};
        }}

        .workflow-stage {{
            border: 1px solid #ced4da; border-radius: 6px; /* Slightly smaller border-radius */ background-color: #fff;
            padding: 8px; /* Slightly reduced padding */ transition: all 0.3s ease;
            display: flex; flex-direction: column;
            flex-grow: 1; /* Allow stages to grow and take available space */
            flex-basis: 0; /* Important for flex-grow to work properly */
            min-width: 120px; /* Minimum width to prevent stages from becoming too narrow */
            max-width: 300px; /* Max width to prevent stages from becoming too wide */
            height: auto; /* Ensure height is determined by content and stretching */
            /* Ensure children (title and steps) can grow within the stage */
            justify-content: space-between; /* Pushes title and steps to ends if desired, or flex-start */
        }}
        
        .workflow-stage.pending {{ border-color: #ced4da; }}
        .workflow-stage.current {{ border-color: #0d6efd; box-shadow: 0 0 8px rgba(13, 110, 253, 0.2); border-width: 2px; padding: 7px;}} /* Adjusted padding for current */
        .workflow-stage.completed {{ border-color: #198754; background-color: #f6fff9; }}
        .workflow-stage.failed {{ border-color: #dc3545; background-color: #fff6f6; }}

        .stage-title {{ font-weight: bold; font-size: 11px; /* Slightly smaller font */ color: #495057; margin-bottom: 6px; padding-bottom: 4px; border-bottom: 1px solid #e9ecef; }}
        .workflow-stage.current .stage-title {{ color: #0d6efd; }}
        .workflow-stage.completed .stage-title {{ color: #198754; }}
        .workflow-stage.failed .stage-title {{ color: #dc3545; }}

        .stage-steps-container {{
            display: flex;
            flex-direction: row; /* Steps arrange horizontally first */
            flex-wrap: wrap; /* Allow steps to wrap within a stage */
            gap: 4px 8px; /* Reduced gap between steps */
            justify-content: flex-start;
            align-items: center;
        }}
        .workflow-step {{
            display: flex; align-items: center; font-size: 10px; /* Smaller font for steps */
            padding: 1px 3px; border-radius: 3px; /* Reduced padding and border-radius */
            flex-shrink: 0; /* Prevent steps from shrinking too much */
        }}
        .workflow-step span {{
            max-width: 100px; /* Adjusted max-width for step name to ensure wrapping */
            word-wrap: break-word; /* Ensures long words break and wrap */
            white-space: normal; /* Allow normal white-space handling, enabling wrapping */
        }}
        .step-icon {{ margin-right: 4px; display: flex; align-items: center; }} /* Reduced margin */
        .step-icon svg {{ width: 10px; height: 10px; }} /* Smaller icons */
        #workflow-display-container.rtl .workflow-step .step-icon {{ margin-right: 0; margin-left: 4px; }}

        .workflow-step.pending {{ color: #6c757d; }}
        .workflow-step.current {{ color: #0d6efd; font-weight: bold; background-color: #e7f1ff; }}
        .workflow-step.completed {{ color: #198754; }}
        .workflow-step.failed {{ color: #dc3545; background-color: #f8d7da; }}
        .workflow-step.current .step-icon {{ animation: pulse-icon 1.5s infinite; }}

        .stage-separator {{
            display: flex;
            align-items: center;
            color: #adb5bd;
            height: 40px; /* Reduced height */
            flex-shrink: 0; /* Prevent separator from shrinking */
        }}
        .stage-separator svg {{
            width: 16px; /* Smaller arrows */
            height: 16px;
            stroke: currentColor;
            stroke-width: 2;
            fill: none;
            transition: transform 0.3s ease;
        }}
        /* For RTL: arrows should point left (opposite direction) */
        #workflow-display-container.rtl .stage-separator svg {{
            transform: rotate(180deg);
        }}

        @keyframes pulse-icon {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.1); }} 100% {{ transform: scale(1); }} }}

        /* Media queries for even smaller screens */
        @media (max-width: 768px) {{
            #workflow-display-container {{
                padding: 5px 10px;
            }}
            .workflow-main-title {{
                font-size: 12px;
                margin-bottom: 5px;
            }}
            .workflow-stage {{
                padding: 5px;
                min-width: 100px;
            }}
            .stage-title {{
                font-size: 10px;
                margin-bottom: 4px;
            }}
            .workflow-step {{
                font-size: 9px;
                padding: 1px 2px;
            }}
            .step-icon svg {{
                width: 9px;
                height: 9px;
            }}
            .stage-separator svg {{
                width: 14px;
                height: 14px;
            }}
        }}

        @media (max-width: 480px) {{
            #workflow-display-container {{
                padding: 3px 5px;
            }}
            .workflow-main-title {{
                font-size: 11px;
                margin-bottom: 3px;
            }}
            .workflow-stage {{
                padding: 4px;
                min-width: 80px;
            }}
            .stage-title {{
                font-size: 9px;
                margin-bottom: 3px;
            }}
            .workflow-step {{
                font-size: 8px;
                padding: 0 1px;
            }}
            .step-icon svg {{
                width: 8px;
                height: 8px;
            }}
            .stage-separator svg {{
                width: 12px;
                height: 12px;
            }}
            .workflow-step span {{
                max-width: 80px; /* Adjust for very small screens */
            }}
        }}
        """
        script = f"""
        if (!document.getElementById('workflow-display-styles')) {{
            const style = document.createElement('style');
            style.id = 'workflow-display-styles';
            style.innerHTML = `{css}`;
            document.head.appendChild(style);
        }}
        """
        self.browserScripting.run_js_script(script_string = script, args = None)

    def _create_workflow_html(self, test_name: str):
        """Creates the initial HTML for the staged workflow display."""
        pending_icon_svg = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"></circle></svg>"""

        # Define a single arrow SVG that points RIGHT (default logical progression)
        # We will rely on CSS transform to flip it for RTL UI flow.
        arrow_svg_right = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>"""

        stages_html = ""

        for i, stage_info in enumerate(self.stages_data):
            steps_html = ""
            for j, step_name in enumerate(stage_info.get('steps', [ ])):
                steps_html += f"""
                <div class="workflow-step pending" id="workflow-step-{i}-{j}">
                    <span class="step-icon">{pending_icon_svg}</span>
                    <span>{step_name}</span>
                </div>
                """

            stages_html += f"""
            <div class="workflow-stage pending" id="workflow-stage-{i}">
                <div class="stage-title">{stage_info.get('stage', f'Stage {i + 1}')}</div>
                <div class="stage-steps-container">{steps_html}</div>
            </div>
            """
            if i < len(self.stages_data) - 1:
                # Always insert the right-pointing arrow SVG. CSS will handle the flip.
                stages_html += f'<div class="stage-separator">{arrow_svg_right}</div>'

        dir_class = 'rtl' if self.direction == 'rtl' else ''
        html = f"""
             <div id="{self.workflow_id}" class="{dir_class}">
                 <div class="workflow-main-title">{test_name}</div>
                 <div class="workflow-stages-wrapper">{stages_html}</div>
             </div>
             """
        script = f"""
        const existing = document.getElementById('{self.workflow_id}');
        if (existing) existing.remove();
        document.body.prepend(document.createRange().createContextualFragment(`{html.strip()}`));
        """
        self.browserScripting.run_js_script(script_string = script, args = None)

    def _adjust_page_layout(self):
        """Adjusts the page's top padding."""
        script = """
        const el = document.getElementById('workflow-display-container');
        if (el) {
            document.body.style.paddingTop = (el.offsetHeight + 10) + 'px';
        }
        """
        self.browserScripting.run_js_script(script_string = script, args = None)

    def _update_visuals(self, stage_index: int, step_index: int, status: str):
        """Updates the UI for a specific step and its parent stage via JavaScript."""
        icons = {
            "pending": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"></circle></svg>""",
            "current": """<svg viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="10"></circle></svg>""",
            "completed": """<svg viewBox="0 0 24 24" fill="none" stroke="#198754" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>""",
            "failed": """<svg viewBox="0 0 24 24" fill="#dc3545" stroke="#fff" stroke-width="1.5"><circle cx="12" cy="12" r="10"></circle><path d="M15 9l-6 6M9 9l6 6"></path></svg>"""
        }

        # JSON encode the data to safely pass it to the JS function
        stages_data_json = json.dumps(self.stages_data)

        script = f"""
        const updateWorkflow = (stagesData, stageIdx, stepIdx, newStatus) => {{
            console.log("updateWorkflow called with:", {{stageIdx, stepIdx, newStatus}}); // DEBUG
            const iconMap = {{
                pending: `{icons[ 'pending' ]}`,
                current: `{icons[ 'current' ]}`,
                completed: `{icons[ 'completed' ]}`,
                failed: `{icons[ 'failed' ]}`
            }};

            // 1. Update the specific step
            const stepId = `workflow-step-${{stageIdx}}-${{stepIdx}}`;
            const stepEl = document.getElementById(stepId);
            console.log(`Looking for step element with ID: ${{stepId}}`, stepEl); // DEBUG
            if (!stepEl) {{
                console.warn(`Step element with ID ${{stepId}} not found.`); // DEBUG
                return;
            }}
            stepEl.className = `workflow-step ${{newStatus}}`;
            stepEl.querySelector('.step-icon').innerHTML = iconMap[newStatus];
            console.log(`Step ${{stepId}} updated to ${{newStatus}}`); // DEBUG


            // 2. Determine and update the stage status
            const stageId = `workflow-stage-${{stageIdx}}`;
            const stageEl = document.getElementById(stageId);
            console.log(`Looking for stage element with ID: ${{stageId}}`, stageEl); // DEBUG
            if (!stageEl) {{
                console.warn(`Stage element with ID ${{stageId}} not found.`); // DEBUG
                return;
            }}

            const stageData = stagesData[stageIdx];
            const stepsInStage = stageEl.querySelectorAll('.workflow-step');
            console.log("Steps in current stage:", stepsInStage); // DEBUG


            let hasFailed = false;
            let allCompleted = true;
            let hasCurrent = false;

            stepsInStage.forEach(s => {{
                if (s.classList.contains('failed')) hasFailed = true;
                if (!s.classList.contains('completed')) allCompleted = false;
                if (s.classList.contains('current')) hasCurrent = true;
            }});

            let newStageStatus = 'pending';
            if (hasFailed) {{
                newStageStatus = 'failed';
            }} else if (allCompleted) {{
                newStageStatus = 'completed';
            }} else if (hasCurrent) {{
                newStageStatus = 'current';
            }} else {{
                // If the first step is completed, but others are pending, consider the stage current.
                // This logic might need refinement based on exact desired behavior for 'current' stage.
                const firstStep = stepsInStage[0];
                if(firstStep && firstStep.classList.contains('completed')){{
                    newStageStatus = 'current';
                }}
            }}
            stageEl.className = `workflow-stage ${{newStageStatus}}`;
            console.log(`Stage ${{stageId}} updated to ${{newStageStatus}}`); // DEBUG

        }};

        // Execute the function with the provided data
        updateWorkflow({stages_data_json}, {stage_index}, {step_index}, '{status}');
        """
        self.browserScripting.run_js_script(script_string = script, args = None)

    @keyword(name = "Define Workflow Stage Steps")
    def define_stage(self, stage_name: str, *steps):
        stage_steps = { "stage": stage_name,
                        "steps": [ ]
                        }
        for step in steps:
            stage_steps[ 'steps' ].append(step)
        return stage_steps

    @keyword(name = "Define Workflow Stags")
    def define_stages(self, *stages_info):
        stages = [ ]
        for stage in stages_info:
            stages.append(stage)
        return stages
