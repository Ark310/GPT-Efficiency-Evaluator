const mongoose = require('mongoose');

const questionSchema = new mongoose.Schema({
    question_text: { type: String, required: true },
    anticipated_answer: { type: String, required: true },
    chatgpt_response: { type: String }
});

module.exports = mongoose.model('Question', questionSchema);
