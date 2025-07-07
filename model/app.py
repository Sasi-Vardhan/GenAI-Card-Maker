import flask
import workflows.prompt_refiner as p # used for making prompt better and all
import workflows.csv_from_prompt as c #used for making format of every card
import cardCreation.imageUrlAdd as imgAdd # used for adding Image url
import support.JsonstringToJson as js #used to convert the response as the json obj
import cardCreation.Html_Code_GEN as htmG #used for making html code for every card
import json
# Currently lets develop for the 

user_prompt=input("please enter what ever and how ever you want your cards to be as our model tries to reach your creative level : ")

number_cards= int(input("Enter number of cards you want to have in your game : "))

print("wait out will be generated model is being processing")

exact_prompt=p.cardPromptRefinement(user_prompt,number_cards) 

"""

#taking the prompt after the user given prompt is refined and all , it will be passed to the next stage in work flows

and model will be included here it shoule have capacity of creating own file/folder structure and process the request on it's own


"""
# print(exact_prompt)
print("----------------------- Format of each Card ----------------------")
string=c.csv_prompt(exact_prompt)
# print(string)

print(type(string))

jsonObj=js.json_to_card_list(string)



print("-------------- Add image URL    -------------------")

# print(type(jsonObj))
jObj=imgAdd.imageUrlAdder(jsonObj)

# print(jObj)

print("-------------- Going for Card Page Generation and all may be using COHERE LLM which is best in giving html structure --------------------- ")

htmG.html_code_gen(jObj)

