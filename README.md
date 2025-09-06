# Data Jobs in Israel Dashboard (2024-2025)

## 📊 Project Overview

The **Data Jobs in Israel Dashboard** is a dynamic web application built with Dash that provides a detailed, up-to-the-minute look at the Israeli job market for key data-related professions. This project aims to empower job seekers, recruiters, and market analysts with actionable insights into the trends and demands of the local data economy.

The dashboard visualizes key metrics for the following roles:
* Data Scientist
* Data Analyst
* Data Engineer
* Business Intelligence (BI) Developer
* Machine Learning Engineer

  **You can view the live dashboard here: [http://artemfedorov.il-central-1.elasticbeanstalk.com/](http://artemfedorov.il-central-1.elasticbeanstalk.com/)**

### Key Findings and Market Insights (as of August 2025)

* **Growth Trajectory:** Contrary to ongoing discourse about AI replacing jobs, the data shows no decline in the demand for data professionals. The average number of new vacancies has seen a consistent increase in recent months.
* **The AI Imperative:** While jobs are not being replaced, the skills required are evolving. "AI" is now mentioned in approximately **30%** of all job postings, reflecting a growing expectation for data professionals to have experience with or knowledge of artificial intelligence concepts and tools.
* **Cloud is the King:** There is a clear upward trend in the number of job descriptions that mention specific cloud platforms (e.g., AWS, GCP, Azure), underscoring the shift towards cloud-native data infrastructure.
* **Geographical Concentration:** The Israeli data job market is highly centralized. More than **75%** of all open positions are located in the Tel Aviv and Central districts, highlighting a significant geographical imbalance.
* **Experience Gap:** The market heavily favors experienced professionals. Only about **7%** of all open positions are designated for students, recent graduates, or junior-level candidates. The average required experience is **3.2 years**.

---

## 🚀 Technical Details

This project is divided into two main components: data collection and visualization.

### Data Collection
The raw data is scraped from Indeed, a leading job board, using `Selenium`. The scraping logic and code are maintained in a separate repository.

* **Scraping Keywords:** The scraper specifically targets job postings containing the keywords: "data scientist", "data analyst", "data engineer", "business intelligence", "machine learning engineer".
* **Skill Extraction:** To accurately identify and categorize required skills from unstructured job descriptions, the text is processed using the **Google Gemini** API. This allows for a more granular and intelligent extraction of skill keywords, providing deeper insights into market demand beyond simple keyword counts.

### Data Visualization
* **Platform:** The dashboard is built using `Dash`, a powerful framework for building analytical web applications in Python.
* **Deployment:** The application is deployed on an AWS Elastic Beanstalk instance, making it accessible to the public.

---

## 🤝 Contribution

I welcome any suggestions or contributions. If you find a bug or have an idea for a new feature, please open an issue or submit a pull request.

