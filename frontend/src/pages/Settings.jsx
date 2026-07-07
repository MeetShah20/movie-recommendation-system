import FriendsSidebar from "../components/FriendsSidebar.jsx";
import { useAuth } from "../auth/AuthContext.jsx";

export default function Settings() {
  const { user } = useAuth();

  return (
    <section className="page settings">
      <h1>Settings</h1>
      {user && <p className="status">Signed in as {user.name} (@{user.username})</p>}
      <div className="settings-layout">
        <FriendsSidebar />
      </div>
    </section>
  );
}
