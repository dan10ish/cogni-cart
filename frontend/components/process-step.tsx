"use client";

import { useEffect, useState } from "react";
import { Loader2, Search, Database, BarChart3, Sparkles, CheckCircle2 } from "lucide-react";

interface ProcessStepProps {
  currentStep?: string;
  allSteps?: string[];
}

export function ProcessStep({ currentStep, allSteps = [] }: ProcessStepProps) {
  const [displayStep, setDisplayStep] = useState("");

  useEffect(() => {
    if (currentStep) {
      setDisplayStep(currentStep);
    }
  }, [currentStep]);

  const getStepIcon = (step: string) => {
    if (step.includes("Understanding") || step.includes("🎯")) return Search;
    if (step.includes("Searching") || step.includes("🚀") || step.includes("database")) return Database;
    if (step.includes("Analyzing") || step.includes("📊")) return BarChart3;
    if (step.includes("Generating") || step.includes("📝")) return Sparkles;
    if (step.includes("✅") || step.includes("ready")) return CheckCircle2;
    return Search;
  };

  const StepIcon = getStepIcon(displayStep);

  return (
    <div className="space-y-3">
      {/* Current Step */}
      {displayStep && (
        <div className="flex items-center gap-3 text-muted-foreground">
          <div className="flex items-center gap-2">
            <StepIcon className="w-4 h-4" />
            <Loader2 className="w-4 h-4 animate-spin" />
          </div>
          <span className="text-sm">{displayStep}</span>
        </div>
      )}

      {/* Previous Steps */}
      {allSteps.length > 1 && (
        <div className="space-y-2 ml-6 border-l-2 border-border/20 pl-4">
          {allSteps.slice(0, -1).map((step, index) => {
            const PrevIcon = getStepIcon(step);
            return (
              <div key={index} className="flex items-center gap-2 text-xs text-muted-foreground/60">
                <PrevIcon className="w-3 h-3" />
                <span>{step}</span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
} 