import { useState, useEffect } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";

export default function Chatbot() {
    const [question, setQuestion] = useState("Tell me about yourself.");
    const [answer, setAnswer] = useState("");
    const [feedback, setFeedback] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const sampleQuestions = [ 
        "Tell me about yourself.",
        "What is your biggest strength?",
        "How do you handle pressure?",
        "Why should we hire you?",
        "Describe a challenging project you've worked on.",
    ];

    // Check Backend Status on Mount
    useEffect(() => {
        axios.get("http://127.0.0.1:8080/")
            .catch(() => setError("Backend is not reachable. Ensure it's running."));
    }, []);

    const handleSubmit = async () => {
        setLoading(true);
        setFeedback("");
        setError("");

        try {
            const response = await axios.post("http://127.0.0.1:8080/evaluate", {
                question: question,
                answer: answer,
            });
            setFeedback(response.data.feedback);
        } catch (err) {
            setError(err.response?.data?.detail || "Something went wrong! Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-8 max-w-2xl mx-auto bg-white/10 backdrop-blur-lg shadow-2xl rounded-3xl border border-gray-300 
                        text-white flex flex-col items-center space-y-6 transition-all duration-500">
            <h1 className="text-4xl font-extrabold text-center bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">
                MockRecruiter AI
            </h1>
            <p className="text-lg text-black text-center">Get AI-powered interview feedback instantly.</p>

            {error && (
                <motion.div 
                    initial={{ opacity: 0, y: 10 }} 
                    animate={{ opacity: 1, y: 0 }} 
                    transition={{ duration: 0.4 }} 
                    className="mt-6 p-4 bg-red-500/20 border-l-4 border-red-400 text-black rounded-xl shadow"
                >
                    {error}
                </motion.div>
            )}

            <div className="w-full">
                <label className="font-medium text-black">Select a Question:</label>
                <select
                    className="w-full mt-2 p-3 border border-gray-500 rounded-xl bg-black/30 text-white focus:ring-2 focus:ring-blue-400"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                >
                    {sampleQuestions.map((q, index) => (
                        <option key={index} value={q} className="bg-gray-800 text-white">
                            {q}
                        </option>
                    ))}
                </select>
            </div>

            <div className="w-full">
                <label className="font-medium text-black">Your Answer:</label>
                <textarea
                    className="w-full mt-2 p-3 border border-gray-500 rounded-xl bg-black/30 text-white focus:ring-2 focus:ring-blue-400"
                    placeholder="Type your response here..."
                    value={answer}
                    onChange={(e) => setAnswer(e.target.value)}
                />
            </div>

            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className={`px-6 py-3 rounded-xl font-semibold tracking-wide transition-all flex items-center justify-center 
                            ${loading ? "bg-gray-500 cursor-not-allowed" : "bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white"}`}
                onClick={handleSubmit}
                disabled={loading || !answer.trim()}
            >
                {loading ? <Loader2 className="animate-spin mr-2" /> : "Submit Answer"}
            </motion.button>

            {feedback && (
                <motion.div 
                    initial={{ opacity: 0, y: 10 }} 
                    animate={{ opacity: 1, y: 0 }} 
                    transition={{ duration: 0.4 }} 
                    className="mt-6 p-4 bg-green-500/20 border-l-4 border-green-400 text-black rounded-xl shadow"
                >
                    <strong>Feedback:</strong> {feedback}
                </motion.div>
            )}
        </div>
    );
}
