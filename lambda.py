import json
import boto3
import os
import base64

aws_region = os.environ.get('AWS_REGION', 'us-east-1')
polly_client = boto3.client('polly', region_name=aws_region)
bedrock_agent_runtime_client = boto3.client("bedrock-agent-runtime", region_name=aws_region)

KNOWLEDGE_BASE_ID = ""
MODEL_ARN = f"arn:aws:bedrock:{aws_region}::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        user_question = body.get("question")

        if not user_question:
            raise ValueError("Pergunta (texto) não encontrada.")

        response = bedrock_agent_runtime_client.retrieve_and_generate(
            input={'text': user_question},
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': KNOWLEDGE_BASE_ID,
                    'modelArn': MODEL_ARN,
                    'generationConfiguration': {
                        'promptTemplate': {
                            'textPromptTemplate': "Você é um assistente prestativo que responde em português do Brasil. Baseado no contexto a seguir, responda a pergunta do usuário. Se a resposta não estiver no contexto, diga que não sabe a informação.\n\nContexto: $search_results$\n\nPergunta: $user_input$\n\nResposta:"
                        }
                    }
                }
            }
        )
        final_answer_text = response['output']['text']

        polly_response = polly_client.synthesize_speech(
            Text=final_answer_text,
            OutputFormat='mp3',
            VoiceId='Vitoria'
        )
        audio_stream = polly_response['AudioStream'].read()
        
        # Cria o corpo da resposta com o áudio em base64
        response_body = {
            "audioBase64": base64.b64encode(audio_stream).decode('utf-8')
        }

        # Retorna um JSON simples.
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST',
                'Content-Type': 'application/json' 
            },
            'body': json.dumps(response_body)
        }

    except Exception as e:
        error_response = {'error': f'Erro interno no servidor: {str(e)}'}
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST',
                'Content-Type': 'application/json' 
            },
            'body': json.dumps(error_response, ensure_ascii=False)
        }