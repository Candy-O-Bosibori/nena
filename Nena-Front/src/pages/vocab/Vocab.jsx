import React, { useState, useEffect } from 'react';
import { FaTrash, FaEdit, FaCheck, FaTimes } from 'react-icons/fa';
// import jwtDecode from 'jwt-decode';
import { API_BASE_URL } from '../../utils/apiBase';

export const Vocab = () => {
  const [words, setWords] = useState([]);
  const [newWord, setNewWord] = useState('');
  const [editingWordId, setEditingWordId] = useState(null);
  const [editingWordText, setEditingWordText] = useState('');

  // Fetch words from API
  useEffect(() => {
    const fetchWords = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) return;

      try {
        const response = await fetch(`${API_BASE_URL}/words`, {
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

    const token = localStorage.getItem('access_token');
    try {
      const response = await fetch(`${API_BASE_URL}/words`, {
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
    const token = localStorage.getItem('access_token');
    try {
      const response = await fetch(`${API_BASE_URL}/wordsById/${id}`, {
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

    const token = localStorage.getItem('access_token');
    try {
      const response = await fetch(`${API_BASE_URL}/wordsById/${id}`, {
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
    <div className="min-h-screen bg-cream">
      <div className="mx-auto w-full max-w-3xl px-5 py-10">
        <header className="mb-8">
          <h1 className="font-display text-3xl font-normal tracking-tight text-ink md:text-4xl">
            Vocabulary
          </h1>
          <p className="mt-2 text-sm text-ink-soft">
            Words you&rsquo;re learning. We highlight them when you use them in a session.
          </p>
        </header>
      {/* Add new word */}
      <div className="flex mb-6 gap-2">
        <input
          type="text"
          value={newWord}
          onChange={e => setNewWord(e.target.value)}
          placeholder="Enter new word"
          className="flex-1 rounded-xl border border-line bg-cream px-4 py-2.5 text-sm text-ink placeholder:text-ink-muted transition-colors focus:border-primary focus:bg-surface focus:outline-none"
        />
        <button
          onClick={handleAddWord}
          className="rounded-xl bg-primary px-5 py-2.5 text-sm font-bold text-on-primary transition-all duration-200 hover:bg-primary-hover active:scale-[0.98] focus-ring"
        >
          Add
        </button>
      </div>

      {/* Words list */}
      <ul className="space-y-3">
        {words.map(word => (
          <li
            key={word.id}
            className="flex items-center justify-between rounded-xl border border-line bg-surface p-3.5 transition-all duration-200 hover:border-ink-muted/40 hover:shadow-sm"
          >
            {editingWordId === word.id ? (
              <>
                <input
                  type="text"
                  value={editingWordText}
                  onChange={e => setEditingWordText(e.target.value)}
                  className="flex-1 rounded-lg border border-line bg-cream px-3 py-2 text-sm text-ink transition-colors focus:border-primary focus:bg-surface focus:outline-none"
                />
                <div className="flex gap-2 ml-4">
                  <button
                    onClick={() => handleSaveEdit(word.id)}
                    className="text-primary hover:text-primary-hover"
                  >
                    <FaCheck />
                  </button>
                  <button
                    onClick={() => setEditingWordId(null)}
                    className="text-danger hover:opacity-80"
                  >
                    <FaTimes />
                  </button>
                </div>
              </>
            ) : (
              <>
                <span className="font-semibold text-ink">{word.word}</span>
                <div className="flex gap-3">
                  <button
                    onClick={() => handleEditWord(word)}
                    className="text-secondary hover:text-secondary-hover"
                  >
                    <FaEdit />
                  </button>
                  <button
                    onClick={() => handleDeleteWord(word.id)}
                    className="text-danger hover:opacity-80"
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


