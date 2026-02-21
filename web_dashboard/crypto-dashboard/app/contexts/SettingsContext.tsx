"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
  ReactNode,
} from "react";

type AIModel = "VADER (Fast)" | "FinBERT (Accurate)";

interface SettingsContextType {
  aiModel: AIModel;
  setAIModel: (model: AIModel) => void;
}

const SettingsContext = createContext<SettingsContextType | undefined>(
  undefined
);

export function SettingsProvider({ children }: { children: ReactNode }) {
  const [aiModel, setAIModelState] = useState<AIModel>(() => {
    if (typeof window !== "undefined") {
      const savedModel = localStorage.getItem("aiModel") as AIModel;
      return savedModel || "VADER (Fast)";
    }
    return "VADER (Fast)";
  });

  useEffect(() => {
    localStorage.setItem("aiModel", aiModel);
  }, [aiModel]);

  const setAIModel = (model: AIModel) => {
    setAIModelState(model);
  };

  return (
    <SettingsContext.Provider value={{ aiModel, setAIModel }}>
      {children}
    </SettingsContext.Provider>
  );
}

export function useSettings() {
  const context = useContext(SettingsContext);

  if (context === undefined) {
    throw new Error("useSettings must be used within a SettingsProvider");
  }

  return context;
}
