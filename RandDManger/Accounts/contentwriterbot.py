from openai import OpenAI
from .models import UserAdmin,HomeInfo,ContentCreator,Types,Style,TargetAudience
### create image generation pipeline ###
# Importing the necessary modules
# from django.apps import apps
# from .intialized import initialize_pipeline
# from .apps import MyAppConfig
# from diffusers import DiffusionPipeline
# import torch
import io
from PIL import Image
import requests


class ContentWriterBot:
    def __init__(self):
        try:
            self.client = OpenAI()
            self.API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
            self.headers = {"Authorization": "Bearer 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"}
            # self.pipeline=initialize_pipeline()
            # self.pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16,local_files_only=True,return_cached_folder = True)
            # Move the pipeline to GPU if available
            # if torch.cuda.is_available():
            #     self.pipeline.to("cuda")
        
        # self.message_properties_request=message_properties_request 
        # self.message=""
        except Exception as e:
            print("Error:", e)

        
        
        
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
        elif types.type=="SOCIAL MEDIA POST CONTENT":
            format="start with a title then seperate line and seperated paragraphs with seperated lines for social media post"



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
        content_type=types.type
        return plaintext_message,content_type
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
                
    def format_social_post(self,lines):
        lines = [line.strip() for line in lines.split('!') + lines.split('?') + lines.split('.') +lines.split('-')]

        # Remove empty lines
        lines = [line for line in lines if line]
        title=lines[0]
        paragraph=lines[1:]
        return title,paragraph




    def format_result(self, lines):
        
        # Generate HTML code for the table
        html_table = "<table border='1'>\n"
        html_table += "<tr><th>Scene</th><th>Visual</th><th>Voice Over</th></tr>\n"
        scene_number=1
        visual=""
        voice_over=""
        # lines=lines
        data=[]
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
                    data.append([scene_number,visual,voice_over])

        html_table += "</table>"

        print(html_table)
        
        return html_table
        #return html_table,data



    def generate_image(self, prompt):
        prompt_json =({"inputs": "{}".format(prompt)})
        response = requests.post(self.API_URL, headers=self.headers, json=prompt_json)
	    # You can access the image with PIL.Image for example
        image = Image.open(io.BytesIO(response.content))
        return image
        # Define the negative prompt
        # negative_prompt = '3d, cartoon, anime, sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ' + \
        #                 '((grayscale)) Low Quality, Worst Quality, plastic, fake, disfigured, deformed, blurry, bad anatomy, blurred, watermark, grainy, signature'

        # # Get the instance of the application config
        # myapp_config = apps.get_app_config('Accounts')

        # # Access the image pipeline attribute from the application config
        # image_pipeline = myapp_config.image_pipeline

        # Generate the image using the pipeline and provided prompt
        # pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5",use_safetensors=True, torch_dtype=torch.float16)
        # img = pipeline(prompt, negative_prompt=negative_prompt).images[0]

        # Save the generated image to a file
        # img.save('/content/photo.png')

        # Return the generated image
        



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
