import React, { createContext, useState, useEffect } from "react";

export const UserContext = createContext();

export default ({ children }) => {
  const [user, setUser] = useState("");
  const [token, setToken] = useState("");
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    setUser({});
    setToken("");
    setAuthenticated(false);
  }, []);

  return (
    <UserContext.Provider
      value={{
        user,
        setUser,
        token,
        setToken,
        authenticated,
        setAuthenticated,
      }}
    >
      {children}
    </UserContext.Provider>
  );
};
