"use client";

import { useEffect, useState } from "react";
import { Loader2, Search, Database, BarChart3, Sparkles } from "lucide-react";

const processSteps = [
  { icon: Search, text: "Understanding your query..." },
  { icon: Database, text: "Searching product database..." },
  { icon: BarChart3, text: "Analyzing products..." },
  { icon: Sparkles, text: "Generating recommendations..." },
];

export function ProcessStep() {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev + 1) % processSteps.length);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const CurrentIcon = processSteps[currentStep].icon;

  return (
    <div className="flex items-center gap-3 text-muted-foreground">
      <div className="flex items-center gap-2">
        <CurrentIcon className="w-4 h-4" />
        <Loader2 className="w-4 h-4 animate-spin" />
      </div>
      <span className="text-sm">{processSteps[currentStep].text}</span>
    </div>
  );
} 