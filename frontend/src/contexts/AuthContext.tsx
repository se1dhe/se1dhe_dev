import React, { createContext, useContext, useState, useEffect } from 'react';

interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isAdmin: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    // TODO: Check for existing session/token
    const checkAuth = async () => {
      try {
        // const response = await fetch('/api/auth/check');
        // const data = await response.json();
        // if (data.user) {
        //   setUser(data.user);
        // }
      } catch (error) {
        console.error('Auth check failed:', error);
      }
    };

    checkAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      // TODO: Implement actual API call
      // const response = await fetch('/api/auth/login', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ email, password }),
      // });
      // const data = await response.json();
      // if (data.user) {
      //   setUser(data.user);
      // } else {
      //   throw new Error(data.message || 'Login failed');
      // }

      // Temporary mock login
      setUser({
        id: 1,
        name: 'John Doe',
        email: email,
        role: email.includes('admin') ? 'admin' : 'user',
      });
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const logout = () => {
    // TODO: Implement actual logout API call
    setUser(null);
  };

  const value = {
    user,
    isAuthenticated: !!user,
    isAdmin: user?.role === 'admin',
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}; 