 Project Title
ChefMate: Restaurant Clustering & Cooking Guide Application

Skills Gained
- Streamlit Application Development  
- Machine Learning (Clustering)  
- AWS Services: S3, RDS, EC2  
- Data Cleaning & Preprocessing  
- Integrating ML Models into Web Applications  
- Building Conversational Chatbots  
 

Domain
Food and Beverages | Machine Learning & AI | Cloud Computing


Problem Statement

**ChefMate** is an intelligent web application that clusters and recommends restaurants based on user preferences and cuisine types. 
Additionally, it integrates a **conversational chatbot** that guides users through recipe preparation — bringing the experience of a virtual chef to users' fingertips.


Business Use Cases

-  Personalized restaurant recommendations tailored to user preferences  
- Interactive maps and ratings for enhanced UX  
-  Real-time chatbot support for home cooking guidance  
-  Potential integration with food delivery platforms for business scaling  


 Approach & Architecture

1.  Data Handling
- **Source**: Zomato JSON dataset
- Upload raw data to **AWS S3**
- Clean & preprocess data after pulling from S3
- Store structured tables in **AWS RDS (PostgreSQL/MySQL)**

 2.  Machine Learning
- Apply **clustering algorithms** (e.g., KMeans) on restaurant data  
- Group restaurants by similarity in cuisine, location, price, and ratings  

 3.  Conversational Chatbot
- A **chef-like assistant** built using rule-based or NLP-based models  
- Assists users in cooking by walking them through recipe steps  

4.  Streamlit Web Application
- Input filters: Cuisine, Location, Dish Name  
- Output: Clusters of restaurants with maps and ratings  
- Integrated chatbot for recipe help  
- **Hosted on AWS EC2** for real-time access  



 Results

-  Restaurant recommendation engine based on clustering  
-  Map integration and restaurant visualizations  
-  Real-time recipe assistant chatbot  
-  Deployed application on **AWS EC2** with backend in **RDS + S3**



Tech Stack

- **Python**  
- **Streamlit**  
- **AWS S3, RDS, EC2**  
- **Pandas, Scikit-learn**  
- **NLP/Chatbot Frameworks (optional)**  
- **Folium / Plotly for Maps**  



