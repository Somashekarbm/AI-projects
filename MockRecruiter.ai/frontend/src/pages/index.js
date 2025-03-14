import Chatbot from "./chatbot"; // Adjust path if needed

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6">
      <h1 className="text-2xl font-bold">Welcome to MockRecruiter</h1>
      <Chatbot />
    </div>
  );
}