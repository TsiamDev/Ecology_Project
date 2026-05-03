<img width="3238" height="3000" alt="ecology_project" src="https://github.com/user-attachments/assets/04f07f71-1ead-4702-a09e-1fb2a0f25193" />


# Ecology_Project

# Summary
Over the past few days, I designed and developed an ecology project focused on monitoring the growth and health of a Sansevieria plant using a RGB camera system.
The setup allowed me to capture high-resolution images at regular intervals, allowing for the observation of subtle changes in leaf coloration, structure, and overall the plant's vitality. By combining consistent imaging with controlled environmental conditions, the project generated a visual dataset that can support future analysis on plant stress responses, growth patterns, and ecological interactions.
This work demonstrates how simple optical tools can provide meaningful insights into plant behavior and environmental interactions.

# Technical Description
The project's analytical framework combines foundational image processing techniques with emerging AI-driven methods to extract meaningful ecological insights from the captured RGB imagery. Each frame enters a processing pipeline built with OpenCV, where it undergoes resizing, color-space normalization, and extraction of per-channel histograms. These histograms quantify shifts in brightness and color distribution, enabling early detection of subtle changes in leaf pigmentation that may signal stress or growth variation.
Following preprocessing, the dataset is segmented using an unsupervised k-means clustering algorithm. By grouping pixels based on color similarity, k-means effectively isolates the plant from the background and highlights internal leaf regions with distinct chromatic or textural characteristics. This segmentation supports more precise tracking of morphological changes over time and provides a structured foundation for downstream analysis.
Looking ahead, the computational pipeline can be strengthened by expanding the AI component. While k-means offers reliable baseline segmentation, future iterations may incorporate deep learning models, such as convolutional neural networks, to classify stress states, detect anomalies, or predict growth trajectories based on temporal patterns. Training these models on the current dataset—augmented with additional labeled samples—would enable more automated, accurate, and scalable ecological assessments, ultimately transforming the system into a predictive tool rather than a purely observational one.
