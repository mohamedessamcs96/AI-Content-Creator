from openai import OpenAI
from .models import UserAdmin,HomeInfo,ContentCreator,Types,Style,TargetAudience




class ContentWriterBot:
    def __init__(self):
        self.client = OpenAI(api_key="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")
        # self.message_properties_request=message_properties_request 
        # self.message=""
        
        
        
    def resample_message(self,message_properties_request):
        subject = message_properties_request.POST['subject']
        purpose = message_properties_request.POST['purpose']
        word_count = message_properties_request.POST['word_count']
        message = message_properties_request.POST['message']

        # Retrieve the related objects based on IDs
        type_id = message_properties_request.POST['types']
        target_audience_id = message_properties_request.POST['target_audience']
        style_id = message_properties_request.POST['style']

        try:
            # Retrieve the actual objects
            types = Types.objects.get(pk=type_id)
            target_audience = TargetAudience.objects.get(pk=target_audience_id)
            style = Style.objects.get(pk=style_id)
            
            # Now you have the related objects, you can use them in your logic
            # For example:
            # type_name = types.name  # Accessing the name field of Types

        except Types.DoesNotExist:
            # Handle the case where the Types object does not exist
            pass
        except TargetAudience.DoesNotExist:
            # Handle the case where the TargetAudience object does not exist
            pass
        except Style.DoesNotExist:
            # Handle the case where the Style object does not exist
            pass

        format=""
        if types.type == "Video Content Script":
            format="start with a title then mention three things the scence number visual and voice over"
        print("format",format)

        # format=""
        # if types.type == "Video Content Creator":
        #     print("format",format)
        #     format="constist of title then three paragraphs an Introduction,middle and ending and should every pargraph start with the three words"
        # print("format",format)
        plaintext_message = """Give me an {} {} , it's subject  is {} for audience between {} 
        it's  purpose is {} and the word count should be {} and the message should be {} and it's made for {}
        """.format(types,format,subject,target_audience,purpose,word_count,message,style)
        print(plaintext_message)
        # Split the text into individual scenes
        
        return plaintext_message
        # self.generate_response(plaintext_message)
        #self.message=
    


    def generate_response(self, message):
        # Construct the conversation
        # message=self.resample_message(self.plaintext_message)
        conversation = [
            {"role": "system", "content": "You are an assistant as a Content Writer."},
            {"role": "user", "content": message},
        ]

        try:
            # Send the conversation to OpenAI API
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )
        
            return completion.choices[0].message
        
        except Exception as e:
            print("Error:", e)
            return "An error occurred while processing your request."

# # Example usage:
# if __name__ == "__main__":
#     api_key = "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"
        

    def format_result(self, lines):

        scene = lines.count("Visual:")


        # Generate HTML code for the table
        html_table = "<table border='1'>\n"
        html_table += "<tr><th>Scene</th><th>Visual</th><th>Voice Over</th></tr>\n"
        scene_number=1
        visual=""
        voice_over=""
        lines=lines
        # Iterate through each scene and parse the content
        # for index, line in enumerate(lines): 
        #     if "Visual:" in line:
        #         scene_number = index
        #         visual = lines[index+1]
        #         # Construct the row of the HTML table
        #         html_table += f"<tr><td>{scene_number}</td><td>{visual}</td><td>{voice_over}</td></tr>\n"

        #     if "Voiceover:" in line:
        #         scene_number = index
        #         voice_over = lines[index+1]
        #         # Construct the row of the HTML table
        #         html_table += f"<tr><td>{scene_number}</td><td>{visual}</td><td>{voice_over}</td></tr>\n"

        scene_number=0
        for  line in lines: 
            if line.startswith("Visual:"):                
                visual = line.replace("Visual:", "")
                # Construct the row of the HTML table
            if line.startswith("Voice Over:"):
                voice_over = line.replace("Voice Over: ", "")
                # Construct the row of the HTML table
                        # Construct the row of the HTML table only if both visual and voice_over are not empty
                if visual and voice_over:
                    scene_number +=1
                    html_table += f"<tr><td>{scene_number}</td><td>{visual}</td><td>{voice_over}</td></tr>\n"

            
            # html_table += f"<tr><td>{scene_number}</td><td>{visual}</td><td>{voice_over}</td></tr>\n"

           

        html_table += "</table>"

        print(html_table)
        
        return html_table





# def content_writer_bot(user_input):
#     # Construct the conversation
#     try:
#         client = OpenAI(api_key="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")
#         print(client)
#     except Exception as e:
#         print("Error:", e)
#         print("Please check your API key.")
#     conversation = [
#         {"role": "system", "content": "You are an assistant as a Content Writer."},
#         {"role": "user", "content": user_input},
#     ]

#     try:
#         # Send the conversation to OpenAI API
#         completion = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=conversation
#         )

#         # Print the generated message from the API response
#         return completion.choices[0].message
#     except Exception as e:
#         print("Error:", e)
#         return "An error occurred while processing your request."
