import { Link } from "react-router-dom";

export default function FriendsSidebar({ signedIn, friends, loading }) {
  if (!signedIn) {
    return (
      <aside className="sidebar">
        <h2 className="sidebar-title">Friends</h2>
        <p className="status">
          <Link to="/login">Sign in</Link> to add friends.
        </p>
      </aside>
    );
  }

  return (
    <aside className="sidebar">
      <h2 className="sidebar-title">Friends</h2>
      {loading && <p className="status">Loading...</p>}
      {!loading && friends.length === 0 && <p className="status">No friends yet.</p>}
      <ul className="friend-list">
        {friends.map((friend) => (
          <li key={`${friend.kind}-${friend.id}`} className="friend">
            <span className="friend-name">{friend.name}</span>
            <span className="friend-kind">{friend.kind === "profile" ? "Viewer" : "Member"}</span>
          </li>
        ))}
      </ul>
    </aside>
  );
}
