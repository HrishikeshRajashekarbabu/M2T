# M2T
Final - A task productivity python bot that captures and routes updates from Monday.com to Telegram groups

Synopsis

Our final project consisted of many ups and downs with a steep learning curve towards the end on how to debug and write efficient code. A tool that we found useful for this was Chat GPT, and with today's advancements in AI and technical ability, it's easy to see how Chat GPT and other such AI-coding software will see immense popularity in the coming decades. Our goals for this challenge were to first ensure that we develop a bot that can consistently deliver updates upon changes to the Monday.com dashboard (which in this case was an example VC dashboard highlighting deals in the different stages of its lifecycle), however, more importantly, we wanted to ensure we can deliver the data in a concise and structured way so as to highlight critical information meant for our Telegram endpoints. For this reason, we decided to relay the updates via a Telegram bot and utilize as much relevant information that can be gathered from the Monday.com API.

Why did we do this:

One of our contributors works as an investment anaylst at a VC firm, and saw that there were severe discrepancies in regards to the flow of updated information, as well as a lack of automation between planning and communication tools. Hence, our project, by capturing updated information on tasks and deals via Monday.com, we could relay that information accordingly to the respective Telegram groups. We saw an opportunity to automate an internal workflow process and use our problem-solving skills to innovate a recurring issue we see in real-life business.

User Instructions:
There are several python packages and modules that we used that require installation -
1. Pandas
2. Datetime
3. Telegram
4. Colorama
5. Collections

Implementation Information

For finding your Monday.com API Developer key. Go to your Monday.com dashboard, click on the bottom left icon highlighting your initials, then Developers > Developer > My Access Tokens

For getting your Telegram.com API KEY. Open Telegram, message botfather - /start - followed by - /newbot - This will allow you to name your bot and then the API token will be given to you

![image](https://user-images.githubusercontent.com/27936494/206092708-434b58bc-169f-40cc-b7f4-b0b8878a54d0.png)

Results :

Very happy with our results, it sends the maximum amount of relvant/required information from Monday.com to Telegram user groups

![image](https://user-images.githubusercontent.com/27936494/206092464-519e40f2-87b2-4ca2-b83e-297a565d5a5b.png)

Project Evolution:

To begin with, we knew that we wanted to create a practical tool that solved a real issue within a professional organization. Given a member of the team works at a VC, we were well aware of administrative / workforce management process flow that could be automated. We spoke to OP Crypto VC about what some issues that were low hanging fruit, could be automated and used a lot of time and we realized that the daily updates (currently done manually, could be automated). There was a specific focus on Initial Due Diligence deals that had not been reviewed over the past 48 hours to ensure that they maintain a speedy pace (the essence of winning new deals and staying competitive in the world of VC).

Initially, we wanted to solely focus on updating the general team about the number of deals that had not been reviewed for the past 48 hours however as we started coding, we realized there was more we could offer. To begin with, the Monday API gave us all the data we needed to grab important statistics of the workflow board that could be collected to give a general overview of the current state of the deal process (e.g. number of deals labeled Initial DD, number of deals per person, number of deals labeled Get Intro). We also realized that we could automate personal statistics where we could give a broad overview of high level statistics and then list key KPIs on a per team member basis (that is on the Monday.com board). 

The key challenge here was to figure out how to find the number of deals per person labeled Initial DD that were older than 48 hours - which ended up taking a long time to debug. At one point, we considered removing this element and keeping it high level (total number of Initial Deals past 48 hours) but after a phone call with OP Crypto VC, they stressed that they wanted it on a per person basis. Eventually, we were able to figure this out.

Initially, we considered building a web app, however, OP Crypto mentioned that they mainly use Telegram as an internal communication tool and therefore saw it as a challenge to not only work with one API (Monday.com) but two. Instead of giving these statistics on a web app, we created a telegram bot that sent out messages to update the deal team on the output of our python model.

Here is how you can set the python script to run everyday at a specified time, this is what automates the daily process.

![image](https://user-images.githubusercontent.com/27936494/206093775-ae44037b-bd19-4917-a19b-f2721c2e7c7e.png)


Issues we faced:

Our first significant issue was dealing with importing the monday module, because upon using the monday module, an import error would pop up indicating that there is a possible issue with “circular input” within the file storage. We used a beta version of an AI search engine called Chat GPT to attempt and solve this issue. This is where we spent a bulk of our time attempting to debug, using the command pip freeze to see what has been installed and then further looking at where everything is stored on the laptop. Another solution we found was to import the Monday-sdk-module which for some reason never ended up properly installing on either device. We finally found solace another way by using the API key to query the code via a JSON file. This forced us to learn how to query the appropriate data but was done easily.

Another issue was with how Monday.com used GraphQL to display its data to developers. We had to query our requests using JSON data structures which took a while to understand. We were disappointed that Monday.com doesn't store its "items" underneath "groups" (Image 1 in Appendix) as this restricted us from structuring our data under different groups in the dashboard, this would've made our piecing together our output a lot easier. We circumvented this by creating aggregator functions which grouped the data together under its respective headers.

Appendix:
Image 1: ![image](https://user-images.githubusercontent.com/27936494/206085792-885024bf-e703-482f-8490-56c99fb58952.png)


