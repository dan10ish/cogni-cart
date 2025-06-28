"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Search, Send, Sparkles, Filter, History } from "lucide-react";

interface SearchInterfaceProps {
  onSearch: (query: string) => void;
  isLoading: boolean;
  searchHistory?: string[];
  suggestions?: string[];
}

export function SearchInterface({ onSearch, isLoading, searchHistory = [], suggestions = [] }: SearchInterfaceProps) {
  const [query, setQuery] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);

  const handleSubmit = () => {
    if (query.trim()) {
      onSearch(query.trim());
      setShowSuggestions(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const exampleQueries = [
    "I need a quiet, pet-friendly vacuum cleaner under $300",
    "Find me a laptop for programming and design work",
    "Best noise-canceling headphones for travel",
    "Gaming laptop with good graphics under $1500",
    "Vacuum that works well on hardwood and carpet"
  ];

  const quickFilters = [
    "Electronics", "Home & Garden", "Sports", "Books", "Clothing"
  ];

  return (
    <div className="w-full max-w-4xl mx-auto space-y-4">
      {/* Main Search Input */}
      <Card className="relative">
        <CardContent className="p-4">
          <div className="flex items-start gap-3">
            <div className="flex-1">
              <div className="relative">
                <Textarea
                  value={query}
                  onChange={(e) => {
                    setQuery(e.target.value);
                    setShowSuggestions(e.target.value.length > 0);
                  }}
                  onKeyPress={handleKeyPress}
                  placeholder="Describe what you're looking for... (e.g., 'I need a quiet laptop for programming under $1200')"
                  className="min-h-[60px] resize-none pr-12 text-base"
                  disabled={isLoading}
                />
                <div className="absolute right-3 top-3">
                  <Sparkles className="w-4 h-4 text-blue-500" />
                </div>
              </div>
              
              {/* Search Suggestions */}
              {showSuggestions && suggestions.length > 0 && (
                <div className="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-md shadow-lg">
                  <div className="p-2">
                    <div className="text-xs font-medium text-gray-500 mb-2">Suggestions</div>
                    {suggestions.map((suggestion, index) => (
                      <button
                        key={index}
                        className="w-full text-left p-2 hover:bg-gray-50 rounded text-sm"
                        onClick={() => {
                          setQuery(suggestion);
                          setShowSuggestions(false);
                        }}
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
            
            <Button
              onClick={handleSubmit}
              disabled={isLoading || !query.trim()}
              className="h-[60px] px-6"
            >
              {isLoading ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <>
                  <Search className="w-4 h-4 mr-2" />
                  Search
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Quick Filters */}
      <div className="flex flex-wrap gap-2 justify-center">
        {quickFilters.map((filter) => (
          <Badge
            key={filter}
            variant="outline"
            className="cursor-pointer hover:bg-blue-50 hover:border-blue-300"
            onClick={() => setQuery(prev => prev ? `${prev} in ${filter}` : filter)}
          >
            <Filter className="w-3 h-3 mr-1" />
            {filter}
          </Badge>
        ))}
      </div>

      {/* Example Queries */}
      {query === "" && (
        <div className="text-center space-y-3">
          <div className="text-sm text-gray-600">Try these example searches:</div>
          <div className="flex flex-wrap gap-2 justify-center">
            {exampleQueries.map((example, index) => (
              <button
                key={index}
                className="text-xs bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-full px-3 py-1 transition-colors"
                onClick={() => setQuery(example)}
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Search History */}
      {searchHistory.length > 0 && query === "" && (
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-2 mb-3">
              <History className="w-4 h-4 text-gray-500" />
              <span className="text-sm font-medium text-gray-700">Recent Searches</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {searchHistory.slice(0, 5).map((item, index) => (
                <button
                  key={index}
                  className="text-xs bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 rounded-md px-2 py-1 transition-colors"
                  onClick={() => setQuery(item)}
                >
                  {item.length > 50 ? `${item.substring(0, 50)}...` : item}
                </button>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
} 