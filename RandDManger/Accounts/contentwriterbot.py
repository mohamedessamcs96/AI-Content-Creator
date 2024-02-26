from openai import OpenAI




class ContentWriterBot:
    def __init__(self):
        self.client = OpenAI(api_key="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")
        # self.message_properties_request=message_properties_request 
        # self.message=""
        
        
        
    def resample_message(self,message_properties_request):
        subject=message_properties_request.POST['subject']
        types=message_properties_request.POST['types']
        purpose=message_properties_request.POST['purpose']
        word_count=message_properties_request.POST['word_count']
        message=message_properties_request.POST['message']
        target_audience=message_properties_request.POST['target_audience']
        style=message_properties_request.POST['style']
        
        format=""
        if types=="Video Content Creator":
            format="constist of three paragraphs Introduction,middle and ending"

        plaintext_message = """Give me an {} {} , it's subject  is {} for audience between {} 
        it's  purpose is {} and the word count should be {} and the message should be {} and it's made for {}
        """.format(types,format,subject,target_audience,purpose,word_count,message,style)
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
            

            # Print the generated message from the API response
            return completion.choices[0].message
        except Exception as e:
            print("Error:", e)
            return "An error occurred while processing your request."

# # Example usage:
# if __name__ == "__main__":
#     api_key = "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"
    







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
