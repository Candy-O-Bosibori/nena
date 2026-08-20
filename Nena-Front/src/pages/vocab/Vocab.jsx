import React, { useState, useEffect } from 'react';
import { FaTrash, FaEdit, FaCheck, FaTimes } from 'react-icons/fa';
// import jwtDecode from 'jwt-decode';

export const Vocab = () => {
  const [words, setWords] = useState([]);
  const [newWord, setNewWord] = useState('');
  const [editingWordId, setEditingWordId] = useState(null);
  const [editingWordText, setEditingWordText] = useState('');

  // Fetch words from API
  useEffect(() => {
    const fetchWords = async () => {
      const token = localStorage.getItem('token');
      if (!token) return;

      try {
        const response = await fetch('http://127.0.0.1:5000/words', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) throw new Error('Failed to fetch words');

        const data = await response.json();
        setWords(data);
      } catch (error) {
        console.error('Error fetching words:', error);
      }
    };

    fetchWords();
  }, []);

  // Add new word
  const handleAddWord = async () => {
    if (!newWord.trim()) return;

    const token = localStorage.getItem('token');
    try {
      const response = await fetch('http://127.0.0.1:5000/words', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ word: newWord })
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.error || 'Failed to add word');
      }

      const result = await response.json();
      setWords(prev => [...prev, result.word]);
      setNewWord('');
    } catch (error) {
      console.error('Error adding word:', error);
    }
  };

  // Delete a word
  const handleDeleteWord = async (id) => {
    const token = localStorage.getItem('token');
    try {
      const response = await fetch(`http://127.0.0.1:5000/wordsById/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) throw new Error('Failed to delete word');

      setWords(prev => prev.filter(word => word.id !== id));
    } catch (error) {
      console.error('Error deleting word:', error);
    }
  };

  // Start editing a word
  const handleEditWord = (word) => {
    setEditingWordId(word.id);
    setEditingWordText(word.word);
  };

  // Save edited word
  const handleSaveEdit = async (id) => {
    if (!editingWordText.trim()) return;

    const token = localStorage.getItem('token');
    try {
      const response = await fetch(`http://127.0.0.1:5000/wordsById/${id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ word: editingWordText })
      });

      if (!response.ok) throw new Error('Failed to update word');

      const result = await response.json();
      setWords(prev => prev.map(w => w.id === id ? result.word : w));
      setEditingWordId(null);
      setEditingWordText('');
    } catch (error) {
      console.error('Error updating word:', error);
    }
  };

return (
    <div className="">
      {/* Header */}
      <div className="bg-[#FFEEE3] border border-[#FFEEE3] rounded-md shadow-md p-4 mb-6">
        <h1 className="ml-2 font-semibold text-[#F25019] text-2xl md:text-3xl">
          Vocabulary
        </h1>
      </div>
<div className='p-6 max-w-3xl mx-auto'>
      {/* Add new word */}
      <div className="flex mb-6 gap-2">
        <input
          type="text"
          value={newWord}
          onChange={e => setNewWord(e.target.value)}
          placeholder="Enter new word"
          className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#F25019]"
        />
        <button
          onClick={handleAddWord}
          className="bg-[#F25019] text-white px-4 py-2 rounded-md hover:bg-orange-600 transition"
        >
          Add
        </button>
      </div>

      {/* Words list */}
      <ul className="space-y-3">
        {words.map(word => (
          <li
            key={word.id}
            className="flex items-center justify-between bg-white p-3 rounded-md shadow hover:shadow-lg transition"
          >
            {editingWordId === word.id ? (
              <>
                <input
                  type="text"
                  value={editingWordText}
                  onChange={e => setEditingWordText(e.target.value)}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#F25019]"
                />
                <div className="flex gap-2 ml-4">
                  <button
                    onClick={() => handleSaveEdit(word.id)}
                    className="text-green-500 hover:text-green-700"
                  >
                    <FaCheck />
                  </button>
                  <button
                    onClick={() => setEditingWordId(null)}
                    className="text-red-500 hover:text-red-700"
                  >
                    <FaTimes />
                  </button>
                </div>
              </>
            ) : (
              <>
                <span className="text-gray-800 font-medium">{word.word}</span>
                <div className="flex gap-3">
                  <button
                    onClick={() => handleEditWord(word)}
                    className="text-blue-500 hover:text-blue-700"
                  >
                    <FaEdit />
                  </button>
                  <button
                    onClick={() => handleDeleteWord(word.id)}
                    className="text-red-500 hover:text-red-700"
                  >
                    <FaTrash />
                  </button>
                </div>
              </>
            )}
          </li>
        ))}
      </ul>
      </div>
      
    </div>
  );
};


