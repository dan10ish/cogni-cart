"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Send, Bot, User, ShoppingBag, Github, ExternalLink } from "lucide-react";
import { ProcessStep } from "@/components/process-step";
import { ProductResult } from "@/components/product-result";

interface Product {
  id: string;
  title: string;
  category: string;
  product_type: string;
  price: number;
  rating: number;
  review_count: number;
  brand: string;
  features: string[];
  image_url?: string;
  availability: string;
  review_summary?: string;
  deal_summary?: string;
  url?: string;
}

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  products?: Product[];
  isLoading?: boolean;
  processSteps?: string[];
  currentStep?: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input.trim(),
    };

    setMessages(prev => [...prev, userMessage]);
    const inputQuery = input.trim();
    setInput("");
    setIsLoading(true);

    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      type: 'assistant',
      content: "",
      isLoading: true,
      processSteps: [],
      currentStep: "",
    };

    setMessages(prev => [...prev, assistantMessage]);

    try {
      // Use streaming endpoint
      const response = await fetch("http://localhost:8000/search-stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: inputQuery }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error("No reader available");
      }

      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              
              setMessages(prev => prev.map(msg => 
                msg.id === assistantMessage.id 
                  ? {
                      ...msg,
                      currentStep: data.type === "process" ? data.message : msg.currentStep,
                      processSteps: data.type === "process" 
                        ? [...(msg.processSteps || []), data.message] 
                        : msg.processSteps,
                      isLoading: data.type !== "final" && data.type !== "error",
                      content: data.type === "final" && data.data?.response ? data.data.response : msg.content,
                      products: data.type === "final" && data.data?.products ? data.data.products : msg.products,
                    }
                  : msg
              ));
              
            } catch (e) {
              console.warn("Failed to parse SSE data:", e);
            }
          }
        }
      }

    } catch (error) {
      console.error("Error:", error);
      setMessages(prev => prev.map(msg => 
        msg.id === assistantMessage.id 
          ? {
              ...msg,
              content: "Sorry, I encountered an error. Please make sure the backend is running and try again.",
              isLoading: false,
            }
          : msg
      ));
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const formatMessage = (content: string) => {
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\$([\d,]+\.?\d*)/g, '₹$1')
      .split('\n')
      .map((line, index) => (
        <p key={index} className={line.trim() === '' ? 'h-2' : ''} 
           dangerouslySetInnerHTML={{ __html: line }} />
      ));
  };

  return (
    <div className="flex flex-col h-screen bg-background">
      {/* Sticky Header */}
      <header className="sticky top-0 z-50 border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <ShoppingBag className="w-5 h-5 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-xl font-semibold">CogniCart</h1>
              <p className="text-xs text-muted-foreground">AI-powered shopping assistant</p>
            </div>
          </div>
          
          {/* Header Links */}
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              className="h-9 w-9"
              onClick={() => window.open("https://dan10ish.github.io", "_blank")}
            >
              <User className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              className="h-9 w-9"
              onClick={() => window.open("https://github.com/dan10ish/cogni-cart", "_blank")}
            >
              <Github className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </header>

      <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full">
        <ScrollArea className="flex-1 p-4" ref={scrollAreaRef}>
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                <Bot className="w-8 h-8 text-primary" />
              </div>
              <h2 className="text-2xl font-semibold mb-2">How can I help you shop today?</h2>
              <p className="text-muted-foreground max-w-md">
                I can help you find products, compare options, analyze reviews, and discover the best deals.
              </p>
            </div>
          )}

          <div className="space-y-6">
            {messages.map((message) => (
              <div key={message.id} className="flex gap-3">
                {/* Avatar - Sticky */}
                <div className="w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center sticky top-20">
                  {message.type === 'user' ? (
                    <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                      <User className="w-4 h-4 text-primary-foreground" />
                    </div>
                  ) : (
                    <div className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center">
                      <Bot className="w-4 h-4 text-secondary-foreground" />
                    </div>
                  )}
                </div>
                
                <div className="flex-1 space-y-3">
                  {message.type === 'user' ? (
                    <div className="text-foreground">
                      {message.content}
                    </div>
                  ) : (
                    <>
                      {message.isLoading && (
                        <ProcessStep 
                          currentStep={message.currentStep} 
                          allSteps={message.processSteps || []}
                        />
                      )}
                      
                      {message.content && (
                        <div className="text-foreground space-y-2">
                          {formatMessage(message.content)}
                        </div>
                      )}
                      
                      {message.products && message.products.length > 0 && (
                        <ProductResult products={message.products} />
                      )}
                    </>
                  )}
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>

        {/* Sticky Bottom Input */}
        <div className="sticky bottom-0 border-t border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 p-4">
          <form onSubmit={handleSubmit} className="flex gap-3">
            <div className="flex-1">
              <Textarea
                ref={textareaRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="What are you looking for?"
                className="min-h-[60px] max-h-32 resize-none border-input"
                disabled={isLoading}
              />
            </div>
            <Button
              type="submit"
              disabled={!input.trim() || isLoading}
              size="lg"
              className="h-[60px] px-4"
            >
              <Send className="w-4 h-4" />
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
