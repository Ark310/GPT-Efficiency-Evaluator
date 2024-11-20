const express = require('express');
const mongoose = require('mongoose');
const dotenv = require('dotenv');
const axios = require('axios');
const Question = require('./models/Questions');

dotenv.config();

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;

// MongoDB connection
mongoose
    .connect(process.env.MONGO_URI)
    .then(() => console.log("Connected to MongoDB"))
    .catch((err) => console.error("MongoDB connection error:", err));

// Route to fetch all questions
app.get('/questions', async (req, res) => {
    try {
        const questions = await Question.find();
        res.json(questions);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

// Route to send a question to ChatGPT and save the response
app.post('/questions/:id/chatgpt', async (req, res) => {
    try {
        const question = await Question.findById(req.params.id);
        if (!question) return res.status(404).json({ message: 'Question not found' });

        const startTime = Date.now();

        // Send the question to ChatGPT
        const response = await axios.post('https://api.openai.com/v1/chat/completions', {
            model: "gpt-4",
            messages: [{ role: "user", content: question.question_text }]
        }, {
            headers: { Authorization: `Bearer ${process.env.OPENAI_API_KEY}` }
        });

        const chatgptResponse = response.data.choices[0].message.content;
        const endTime = Date.now();

        // Update the question with ChatGPT's response
        question.chatgpt_response = chatgptResponse;
        await question.save();

        res.json({
            question,
            chatgptResponse,
            responseTime: `${endTime - startTime} ms`
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error communicating with ChatGPT or updating the database' });
    }
});

// Test route to check if environment variables are working
app.get('/test', (req, res) => {
    res.json({
        mongoURI: process.env.MONGO_URI,
        openaiKey: process.env.OPENAI_API_KEY
    });
});


// Start the server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
