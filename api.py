from utils import *

# Return age and feedback (error/multiple detection)
def detect_age_microsoft(picture_link_col):
    col = picture_link_col
    age_data = [[], [], [], [], [], [], [], []]
    
    for image_url in col:
        time.sleep(0.05) # Change to fit API rate specifications
        try:
            if isinstance(image_url, str):
                data = {'url': image_url}
                response = requests.post(FACE_API_URL, params=params, headers=headers, json=data)
                faces = response.json()
                if len(faces) is 1:
                    age_data[0].append(faces[0]["faceAttributes"]["age"])
                    age_data[1].append(faces[0]["faceAttributes"]["blur"]["blurLevel"])
                    age_data[2].append(faces[0]["faceAttributes"]["blur"]["value"])
                    age_data[3].append(faces[0]["faceAttributes"]["exposure"]["exposureLevel"])
                    age_data[4].append(faces[0]["faceAttributes"]["exposure"]["value"])
                    age_data[5].append(faces[0]["faceAttributes"]["noise"]["noiseLevel"])
                    age_data[6].append(faces[0]["faceAttributes"]["noise"]["value"])
                    age_data[7].append(None)
                    print(faces[0]["faceAttributes"]["age"])
                elif len(faces) is 0:
                    for i in range(7):
                        age_data[i].append(None)
                    age_data[7].append("No faces detected")
                else:
                    # Multiple faces
                    for i in range(7):
                        age_data[i].append(None)
                    age_data[7].append("Multiple faces detected")
            else:
                for i in range(7):
                    age_data[i].append(None)
                age_data[7].append("No URL or incorrect format")
        except Exception as e:
            for i in range(7):
                age_data[i].append(None)
            age_data[7].append(faces["error"]["message"])
            print(faces["error"]["message"])
    
    print("Finished using Microsoft Face API.")
    
    return age_data

############## Amazon Credentials ###################################
REKOGNITION_REGION = 'us-west-2'
rekognition = boto3.client("rekognition", aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REKOGNITION_REGION)

############## Amazon Face API detection #########################
def detect_age_amazon(picture_link_col):
    col = picture_link_col
    age_data = []
    for image_url in col:
        try:
            if isinstance(image_url, str):
                response_content = requests.get(image_url).content
                response = rekognition.detect_faces(
                    Image = {
                        'Bytes': response_content
                    },
                    Attributes = ['ALL']
                )
                faces = response['FaceDetails']

                if len(faces) == 1:
                    print(faces[0]['AgeRange'])
                    low = faces[0]['AgeRange']['Low']
                    high = faces[0]['AgeRange']['High']
                    age_data.append([low, high, np.mean([low, high]), None])
                elif len(faces) == 0:
                    age_data.append([None, None, None, 'No face detected'])
                else:
                    age_data.append([None, None, None, 'Multiple face detected'])
            else:
                age_data.append([None, None, None, 'No URL or incorrect format'])
        
        except Exception as e:
            age_data.append([None, None, None, str(e)])
            print(str(e))
        
    print("Finished using Amazon face API.")
        
    return np.vstack(age_data).T

def use_api(excel_file):
    ########## Import Excel file and convert to DataFrame ###############
    excel_file = sys.argv[1]
    xl = pd.ExcelFile(excel_file)
    df = xl.parse('Sheet1')
    df1 = df
    col = df1["LinkPictureNew"]

    ############## Append Microsoft API data to DataFrame ##################
    age_data = detect_age_microsoft(col)

    df1["microsoft_age"] = age_data[0]
    df1["microsoft_blurLevel"] = age_data[1]
    df1["microsoft_blurValue"] = age_data[2]
    df1["microsoft_exposureLevel"] = age_data[3]
    df1["microsoft_exposureValue"] = age_data[4]
    df1["microsoft_noiseLevel"] = age_data[5]
    df1["microsoft_noiseValue"] = age_data[6]
    df1["microsoft_feedback"] = age_data[7]

    ############# Append Amazon API data to excel ######################
    age_data = detect_age_amazon(col)

    df1['amazon_age_low'] = age_data[0]
    df1['amazon_age_high'] = age_data[1]
    df1['amazon_age_avg'] = age_data[2]
    df1['amazon_feedback'] = age_data[3]

    ############# Exporting DataFrame to Excel #########################
    export = excel_file.replace("api_ready.xlsx","api_finished.xlsx")
    writer = pd.ExcelWriter(export, engine='xlsxwriter')    
    df1.to_excel(writer, 'Sheet1', index=False)
    writer.save()
    print("Finished exporting data to excel.")

if __name__ == "__main__":
    # read in excel file and convert to data frame
    excel_file = sys.argv[1]
    use_api(excel_file)
