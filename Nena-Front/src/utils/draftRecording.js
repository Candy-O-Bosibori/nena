// Persists a single in-progress recording (blob + the topic/mode/framework
// context needed to resume) across a sign-up/sign-in navigation. Practice.jsx
// unmounts when we navigate to /signup, which would otherwise drop the blob
// held in React state -- IndexedDB is used because the blob is binary and
// often exceeds localStorage's ~5-10MB string-only quota; localStorage only
// holds the small "is there a pending draft" pointer.

const DB_NAME = "nena-drafts";
const STORE_NAME = "recordings";
const DRAFT_ID_KEY = "pending_draft_id";
const DRAFT_TTL_MS = 24 * 60 * 60 * 1000; // discard drafts older than this

function openDb() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, 1);
    request.onupgradeneeded = () => {
      request.result.createObjectStore(STORE_NAME, { keyPath: "id" });
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

async function withStore(mode, fn) {
  const db = await openDb();
  try {
    return await new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, mode);
      const store = tx.objectStore(STORE_NAME);
      const result = fn(store);
      tx.oncomplete = () => resolve(result);
      tx.onerror = () => reject(tx.error);
    });
  } finally {
    db.close();
  }
}

// meta: { topic, mode, selectedFramework, returnTo }
export async function saveDraft(blob, meta) {
  const id = `draft-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  await withStore("readwrite", (store) => {
    store.put({ id, blob, meta, createdAt: Date.now() });
  });
  localStorage.setItem(DRAFT_ID_KEY, id);
  return id;
}

export function getPendingDraftId() {
  return localStorage.getItem(DRAFT_ID_KEY);
}

export async function loadDraft(id) {
  if (!id) return null;
  const record = await withStore("readonly", (store) => {
    return new Promise((resolve, reject) => {
      const req = store.get(id);
      req.onsuccess = () => resolve(req.result || null);
      req.onerror = () => reject(req.error);
    });
  });
  if (record && Date.now() - record.createdAt > DRAFT_TTL_MS) {
    await deleteDraft(id);
    return null;
  }
  return record;
}

export async function deleteDraft(id) {
  localStorage.removeItem(DRAFT_ID_KEY);
  if (!id) return;
  await withStore("readwrite", (store) => {
    store.delete(id);
  });
}
