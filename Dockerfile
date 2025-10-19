# Use the ppodgorsek/robot-framework image as the base.
FROM ppodgorsek/robot-framework:latest

# --- SETUP AND USER MANAGEMENT ---
# Switch to root to install packages and manage users.
USER root

# Re-create the 'robot' user to prevent "user not found" errors during cross-platform builds.
RUN groupadd -g 1000 robot && \
    useradd -u 1000 -g 1000 -m -s /bin/bash robot

# Install VNC packages for live viewing (Fedora uses dnf)
RUN dnf update -y && \
    dnf install -y x11vnc novnc python3-websockify git && \
    dnf clean all

# Set the working directory (align with base image and run script for consistency).
WORKDIR /opt/robotframework/tests

# Copy requirements.txt if it exists (using wildcard for optional copy)
COPY requirements.tx[t] ./

# --- CONDITIONAL DEPENDENCY INSTALLATION ---
RUN \
  if [ -f requirements.txt ]; then \
    echo "--- Found requirements.txt, installing dependencies with pip. ---"; \
    pip install -r requirements.txt; \
  else \
    echo "--- No requirements.txt found. Creating a template file. ---"; \
    echo "# Add your Python dependencies here" > requirements.txt; \
    echo "# Example Robot Framework dependencies:" >> requirements.txt; \
    echo "# robotframework==6.1.1" >> requirements.txt; \
    echo "# robotframework-seleniumlibrary==6.2.0" >> requirements.txt; \
    echo "# robotframework-browser==18.6.3" >> requirements.txt; \
    echo "# robotframework-requests==0.9.7" >> requirements.txt; \
    echo "--- Template requirements.txt created. Add your dependencies and rebuild. ---"; \
  fi && \
  # Clean up pip cache to keep image lean
  pip cache purge

# Create Results directory with proper permissions
RUN mkdir -p /opt/robotframework/tests/Results/Reports && \
    chown -R robot:robot /opt/robotframework/tests/Results

# Switch back to the non-root 'robot' user for secure execution.
USER robot
