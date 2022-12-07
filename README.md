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

![image](https://user-images.githubusercontent.com/27936494/206089428-603dac73-2d03-419b-8445-6bbe7c42e871.png)

Results :

Very happy with our results, it sends the required informations.

![image](https://user-images.githubusercontent.com/27936494/206090470-d6ae517d-3e55-4059-bf5e-5be13295a000.png)

Project Evolution:


Issues we faced:

Our first significant issue was dealing with importing the monday module, because upon using the monday module, an import error would pop up indicating that there is a possible issue with “circular input” within the file storage. We used a beta version of an AI search engine called Chat GPT to attempt and solve this issue. This is where we spent a bulk of our time attempting to debug, using the command pip freeze to see what has been installed and then further looking at where everything is stored on the laptop. Another solution we found was to import the Monday-sdk-module which for some reason never ended up properly installing on either device. We finally found solace another way by using the API key to query the code via a JSON file. This forced us to learn how to query the appropriate data but was done easily.

Another issue was with how Monday.com used GraphQL to display its data to developers. We had to query our requests using JSON data structures which took a while to understand. We were disappointed that Monday.com doesn't store its "items" underneath "groups" (Image 1 in Appendix) as this restricted us from structuring our data under different groups in the dashboard, this would've made our piecing together our output a lot easier. We circumvented this by creating aggregator functions which grouped the data together under its respective headers.

Appendix:
Image 1: ![image](https://user-images.githubusercontent.com/27936494/206085792-885024bf-e703-482f-8490-56c99fb58952.png)


