# Retrieval-augmented generation por voz com AWS Bedrock e AWS Polly


## Índice

- [Sobre](#sobre)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Funcionalidades Principais](#funcionalidades-principais)
- [Configuração e Execução](#configuração-e-execução)

  ## Sobre

O projeto RAG com Bedrock por Voz na AWS é uma aplicação de Inteligência Artificial moderna e totalmente serverless. A plataforma permite que um usuário faça perguntas por voz sobre uma base de documentos privados e receba uma resposta coesa e contextual, também em formato de áudio, gerada por modelos de IA da Amazon.

## Tecnologias Utilizadas 

Este projeto foi desenvolvido com um conjunto de tecnologias de ponta, focando em uma arquitetura nativa da nuvem, escalável e de baixo custo.

### Frontend

- **JavaScript (Vanilla)**: Lógica de interação, comunicação com a API e manipulação de áudio.
- **Web Speech API**: API nativa do navegador para converter a fala do usuário em texto (Speech-to-Text) sem custo.
- **Web Audio API**: API de baixo nível para decodificar e tocar o áudio da resposta de forma confiável, contornando restrições de autoplay dos navegadores.

### Backend (100% Serverless na AWS)

- **AWS Lambda**: Orquestra todo o fluxo de trabalho no backend, executando o código Python que integra os serviços.
- **Amazon API Gateway**: Provê um endpoint RESTful seguro e escalável para o frontend se comunicar com a Lambda.
- **Amazon S3**: Armazena os documentos (PDFs, TXT, etc.) que formam a base de conhecimento.

### Integração com IA (AWS)

- **Amazon Bedrock (Knowledge Bases)**: Automatiza o processo de RAG (Retrieval-Augmented Generation), buscando informações relevantes nos documentos e utilizando o modelo Anthropic Claude 3 Haiku para gerar respostas em texto.
- **Amazon Polly**: Converte o texto gerado pelo Bedrock em um áudio MP3 com voz natural em português (Text-to-Speech).

## Funcionalidades Principais
**Consulta por Voz a Documentos Privados**: Faça perguntas em linguagem natural e obtenha respostas baseadas exclusivamente no conteúdo dos seus arquivos.
**Respostas em Áudio com IA**: A resposta é sintetizada em uma voz natural e tocada automaticamente, criando uma experiência de conversação.
**Arquitetura Serverless de Baixo Custo**: O custo é estritamente baseado no uso, aproveitando ao máximo o Nível Gratuito da AWS.
**Base de Conhecimento Customizável**: Adapte a IA para qualquer assunto simplesmente trocando os documentos no bucket S3.

## Arquitetura da Solução
<div align="center">
  <img src="https://imgur.com/a/581WfFL.png" alt="fluxo" />
</div>

## Configuração e Execução

Para executar este projeto, é necessário configurar o ambiente na AWS (backend) e o cliente local (frontend).

1. **Escolha a Região Correta**: Todos os recursos devem ser criados na região N. Virginia (us-east-1) para garantir a disponibilidade de todos os modelos de IA.
   
2. **Crie a Base de Conhecimento**:
    -  Crie um bucket no Amazon S3 e faça o upload dos seus documentos.
    - No Amazon Bedrock, crie uma Knowledge Base, aponte para o bucket S3 e deixe o serviço criar o banco de vetores e o perfil IAM automaticamente. Anote o KnowledgeBaseId.
      
3. **Crie a Função Lambda**:
    - Crie uma função Python com um timeout de 30 segundos.
    - Anexe as políticas de IAM necessárias: AmazonPollyFullAccess e uma política em linha para bedrock-agent-runtime:RetrieveAndGenerate no ARN da sua Knowledge Base.
    - Utilize o código Python final fornecido, inserindo o KnowledgeBaseId.
    
4. **Crie a API Gateway**:
    - Crie uma API REST com um recurso (ex: /chat) e um método POST.
    - Configure a integração do POST como Proxy Lambda.
    - Habilite o CORS no recurso.
    - (Opcional, se a Lambda não retornar o áudio diretamente) Em "Configurações", adicione audio/mpeg aos "Tipos de mídia binária".
    -  Faça o Deploy da API para um estágio e copie a URL de Invocação.
      
5. **Executando o Cliente (Frontend)**:
     - **Crie o arquivo index.html**: Salve o código HTML/JavaScript final em um arquivo chamado index.html.
     - **Configure a URL da API**: Dentro do arquivo, cole a URL de Invocação da sua API Gateway na variável apiUrl.
     - **Execute a partir de um Servidor Local (Obrigatório)**: O acesso ao microfone é bloqueado por segurança em arquivos abertos diretamente (file://). É necessário um servidor local.
