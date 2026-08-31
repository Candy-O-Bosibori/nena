import { useEffect, useRef, useState } from 'react';
import { API_BASE_URL } from './apiBase';

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;

// Google's renderButton() draws its own iframe with fixed styling we can't
// theme to match the app, so instead we use initialize()+prompt(): Google's
// SDK still owns the actual sign-in UI (its One Tap prompt / popup), but the
// on-page trigger is our own button, styled like every other button here.
export function useGoogleSignIn({ onSuccess, onError }) {
    const [isReady, setIsReady] = useState(false);
    const callbacksRef = useRef({ onSuccess, onError });
    callbacksRef.current = { onSuccess, onError };

    useEffect(() => {
        if (!GOOGLE_CLIENT_ID) {
            console.error('VITE_GOOGLE_CLIENT_ID is not set; Google sign-in is disabled.');
            return;
        }

        let cancelled = false;

        const init = () => {
            if (cancelled || !window.google?.accounts?.id) return;

            window.google.accounts.id.initialize({
                client_id: GOOGLE_CLIENT_ID,
                callback: async (response) => {
                    try {
                        const res = await fetch(`${API_BASE_URL}/auth/google`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ credential: response.credential }),
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
        if (window.google?.accounts?.id) {
            init();
        } else {
            const interval = setInterval(() => {
                if (window.google?.accounts?.id) {
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
        if (!window.google?.accounts?.id) {
            callbacksRef.current.onError('Google sign-in is still loading. Please try again in a moment.');
            return;
        }
        window.google.accounts.id.prompt((notification) => {
            if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
                callbacksRef.current.onError('Google sign-in was cancelled or blocked by your browser.');
            }
        });
    };

    return { isReady, promptGoogleSignIn };
}
