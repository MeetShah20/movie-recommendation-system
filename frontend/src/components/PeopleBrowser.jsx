import { useEffect, useState } from "react";

import { addFriend, fetchPeople } from "../api/client.js";

export default function PeopleBrowser({ friendKeys, onAdded }) {
  const [search, setSearch] = useState("");
  const [people, setPeople] = useState([]);
  const [busyKey, setBusyKey] = useState(null);

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchPeople(search)
        .then(setPeople)
        .catch(() => setPeople([]));
    }, 300);
    return () => clearTimeout(timer);
  }, [search]);

  async function add(person) {
    const key = `${person.kind}-${person.id}`;
    setBusyKey(key);
    try {
      await addFriend({ kind: person.kind, id: person.id });
      await onAdded();
    } finally {
      setBusyKey(null);
    }
  }

  return (
    <div className="people">
      <h2 className="sidebar-title">Add friends</h2>
      <input
        className="people-search"
        value={search}
        onChange={(event) => setSearch(event.target.value)}
        placeholder="Search people"
        autoComplete="off"
      />
      <ul className="people-list">
        {people.map((person) => {
          const key = `${person.kind}-${person.id}`;
          const added = friendKeys.has(key);
          return (
            <li key={key} className="person">
              <span className="person-name">{person.name}</span>
              <button
                className="person-add"
                type="button"
                disabled={added || busyKey === key}
                onClick={() => add(person)}
              >
                {added ? "Added" : "Add"}
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
