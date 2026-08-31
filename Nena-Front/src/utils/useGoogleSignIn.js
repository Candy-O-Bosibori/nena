import { useEffect, useRef, useState } from 'react';
import { API_BASE_URL } from './apiBase';

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;

// Google's One Tap prompt() looks passive/automatic and silently no-ops in
// common cases (third-party cookies blocked, prior dismissal, incognito) --
// unsuitable for a deliberate button click. initTokenClient instead opens a
// real OAuth popup on click, every time, regardless of those settings.
export function useGoogleSignIn({ onSuccess, onError }) {
    const [isReady, setIsReady] = useState(false);
    const tokenClientRef = useRef(null);
    const callbacksRef = useRef({ onSuccess, onError });
    callbacksRef.current = { onSuccess, onError };

    useEffect(() => {
        if (!GOOGLE_CLIENT_ID) {
            console.error('VITE_GOOGLE_CLIENT_ID is not set; Google sign-in is disabled.');
            return;
        }

        let cancelled = false;

        const init = () => {
            if (cancelled || !window.google?.accounts?.oauth2) return;

            tokenClientRef.current = window.google.accounts.oauth2.initTokenClient({
                client_id: GOOGLE_CLIENT_ID,
                scope: 'openid email profile',
                callback: async (response) => {
                    if (response.error) {
                        callbacksRef.current.onError('Google sign-in was cancelled or blocked by your browser.');
                        return;
                    }
                    try {
                        const res = await fetch(`${API_BASE_URL}/auth/google`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ access_token: response.access_token }),
                        });
                        const data = await res.json();
                        if (!res.ok) {
                            callbacksRef.current.onError(data?.error || 'Google sign-in failed');
                            return;
                        }
                        callbacksRef.current.onSuccess(data);
                    } catch (error) {
                        console.error('Error:', error);
                        callbacksRef.current.onError('Something went wrong. Please try again.');
                    }
                },
            });

            setIsReady(true);
        };

        // The GIS <script> in index.html loads async, so it may not be ready yet.
        if (window.google?.accounts?.oauth2) {
            init();
        } else {
            const interval = setInterval(() => {
                if (window.google?.accounts?.oauth2) {
                    clearInterval(interval);
                    init();
                }
            }, 100);
            return () => {
                cancelled = true;
                clearInterval(interval);
            };
        }

        return () => {
            cancelled = true;
        };
    }, []);

    const promptGoogleSignIn = () => {
        if (!tokenClientRef.current) {
            callbacksRef.current.onError('Google sign-in is still loading. Please try again in a moment.');
            return;
        }
        tokenClientRef.current.requestAccessToken();
    };

    return { isReady, promptGoogleSignIn };
}
