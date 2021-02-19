##Authors
*Divyansh Goyal
*Curtis Silva
*Maheen Hossain
*Mohamed Yassin

##What it does:
AccuVision is a software designed to assist stores, building owners, and consumers alike by tracking the number of people inside of an establishment at any given time and uploading those numbers at pre-determined time intervals to a public dashboard that is viewable by all. To make this possible, the software was made using the OpenCV library which has many real-time computer vision capabilities, from which live data is uploaded on an interactive user interface created through Dash and Plotly. This dashboard features an interactive graph which can be manipulated through selection filters specified by the user, as well as a predictive modelling algorithm to provide recommendations for the user based on their preferences.

It is designed to be implemented in security cameras placed at entrances and exits at stores and businesses to count the number of people entering and leaving the building. The data storage system, powered by Google Drive API, is capable of storing data and displaying the amount of people in the store or business for up to two weeks. This provides consumers with the ability to see trends in the number of people visiting the establishment, so that they can make informed decisions about planning a visit at a time that minimizes potential contact with others, in order to limit their exposure to the COVID-19 virus.

##Inspiration:
The inspiration for AccuVision is to help individuals make informed decisions to reduce the risk of contracting COVID-19. As a result of this pandemic, it has become essential to plan every visit to any establishment so as to limit contact with others. As of now, there does not exist an easy to use and accessible method to track the traffic within buildings. We wanted to create a solution which would allow the general public to view this data as conveniently as possible. We believe that this tool would be especially useful to individuals that are at a higher risk of experiencing harsher symptoms.

Furthermore, this software can be implemented beyond the scope of the coronavirus pandemic, as having this real-time and historical data can enable businesses to make decisions which will allow them to create a higher level of efficiency. Decisions that could be based upon the number of consumers within a business include, managing employee shifts and break times, store hours, and restocking needs. We also wanted to create a solution which is accessible for establishments to use, as they only require a security camera and a computer.

##How we built it:
AccuVision is comprised of two major components, one which collects data and the other which displays it for an overall user-friendly experience.

**Computer Vision:**
The backbone of this project is created using the OpenCV library within Python. Live video feed is taken in as input, upon which frame-by-frame analysis is conducted. In order to do so, we enlisted the help of OpenCV methods to first generate a contour mapping of the detected motion after determining the difference between two consecutive frames. Then, we created a three-boundary system where we initially tracked the direction the individuals are moving in at the center of the frame. Subsequently, the live counter incremented or decremented upon the subject moving to the outer boundary in the direction previously specified. The data collected from the movement is then stored and updated periodically in a database linked with the Google Drive API, which is then displayed onto AccuVision's dynamic user interface.

**User Interface:**
The user interface was created using Dash and Plotly with a goal of enhancing user experience through a simple yet functional design. Initially, data is retrieved from the Google Drive database in the format of a CSV file and stored into dataframes using the Pandas library, which was used due to its powerful data manipulation and analysis capabilities. In order for the user to select different filters and preferences to customize the viewable data, we used callbacks through input elements in Plotly. We then updated certain areas of the dashboard in response to these inputs using various functions. One of the key interactive components include filters for manipulating the viewable data based on the day of the week and the building selected. Another significant feature is to display the day with the least risk of public exposure, according to historical data based on a user-specified time range.

##Built using:
*Python
*OpenCV
*Dash
*Plotly
*Pandas
*HTML
*CSS
*Google Drive API
