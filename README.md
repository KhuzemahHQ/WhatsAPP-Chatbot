# OnlyBusiness

## Motivation

### Problem
Managing WhatsApp businesses is a time-consuming process that involves handling customer queries and requires manual intervention for tasks such as handling orders. These businesses are typically small, with limited resources, making it burdensome for small teams.

### Relevance
WhatsApp business communication is primarily text-based, which presents a significant opportunity to leverage generative AI (genAI) models for automating various aspects of business management. This is especially relevant for small businesses with limited resources, as automation can help them manage larger workloads with fewer personnel.

### Impact
Automating tasks like order processing, customer inquiries, and other routine operations can make businesses more efficient and allow them to focus on growth and customer satisfaction. This can elevate WhatsApp businesses to a new level of professionalism and scalability, helping them compete more effectively in the market.

## Goal
The goal of the project is to empower small businesses by providing them with an efficient solution to manage their workload. Key objectives include:

- **Streamlining Order Management**: Automate order processing, inventory management, and order tracking to reduce manual effort and minimize errors.
- **Boosting Sales**: Improve customer engagement and sales through an automated recommendation system that offers personalized recommendations based on past purchases.
- **Enabling Scalability**: Provide tools and features that support scalability in handling increasing order volumes, expanding product offerings, and catering to a growing customer base without significant additional investment.

## Target Audience
The primary audience includes small business owners and managers who use WhatsApp as their main channel for communication and sales.

## Differentiating Factor
Unlike existing products that mainly leverage chatbot APIs for answering user questions, our product aims to support both the business owner and the customer by providing various order-placement interfaces, a document-based query answering system, and periodic generated reports using sales and chat data.

## Approach
We plan to use the Retriever-Augmented Generation (RAG) to handle most of the customer’s queries based on a document provided by the business owners. Speech inputs will be transcribed into text using a transcription model before further processing. We will test both MMS and Whisper models for this purpose and use the OpenAI assistant API for RAG and function calling. Multilingual support will be handled by prompting the model to respond in the same language as the query.

## Major Use Cases

### Voicenote Capability
Upon receiving a voice note, our system will convert the audio into text using a transcription model. This text is then processed by our Chatbot, utilizing the OpenAI assistant and Google Sheets API to provide accurate responses.

### Manager Reports
The Chatbot acts as a reporting system for managers, autonomously retrieving data from Google Sheets to generate analytical reports. Managers can also query the Chatbot for real-time information, aiding in informed decision-making.

### Recommendation Systems
The bot will offer personalized product recommendations to users based on their past purchases and related products during the order placement process.

### User Reports
Users can interact with the Chatbot to inquire about their past purchases, allowing them to access detailed data analysis and make informed decisions based on their spending habits.
