import { useCallback, useEffect, useState } from "react";

import FriendsSidebar from "../components/FriendsSidebar.jsx";
import PeopleBrowser from "../components/PeopleBrowser.jsx";
import { fetchFriends, removeFriend } from "../api/client.js";
import { useAuth } from "../auth/AuthContext.jsx";

export default function Settings() {
  const { user } = useAuth();
  const [friends, setFriends] = useState([]);
  const [loading, setLoading] = useState(true);

  const reload = useCallback(() => {
    if (!user) {
      setLoading(false);
      return Promise.resolve();
    }
    return fetchFriends()
      .then(setFriends)
      .catch(() => setFriends([]))
      .finally(() => setLoading(false));
  }, [user]);

  useEffect(() => {
    reload();
  }, [reload]);

  async function remove(friend) {
    await removeFriend({ kind: friend.kind, id: friend.id });
    await reload();
  }

  const friendKeys = new Set(friends.map((friend) => `${friend.kind}-${friend.id}`));

  return (
    <section className="page settings">
      <h1>Settings</h1>
      {user && <p className="status">Signed in as {user.name} (@{user.username})</p>}
      <div className="settings-layout">
        <FriendsSidebar signedIn={Boolean(user)} friends={friends} loading={loading} onRemove={remove} />
        {user && <PeopleBrowser friendKeys={friendKeys} onAdded={reload} />}
      </div>
    </section>
  );
}
