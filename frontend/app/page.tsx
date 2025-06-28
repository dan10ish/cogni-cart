"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { SearchInterface } from "@/components/search-interface";
import { ProductCard } from "@/components/product-card";
import { ProductDetailsModal } from "@/components/product-details-modal";
import { ShoppingBag, Brain, Zap, TrendingUp, Users, Award, GitCompare } from "lucide-react";

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
}

interface SearchResult {
  type: string;
  response: string;
  products?: Product[];
  total_products_found?: number;
  parsed_query?: any;
  additional_products?: Product[];
}

export default function Home() {
  const [searchResult, setSearchResult] = useState<SearchResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [searchHistory, setSearchHistory] = useState<string[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [productDetails, setProductDetails] = useState<any>(null);
  const [showModal, setShowModal] = useState(false);
  const [compareList, setCompareList] = useState<string[]>([]);

  // Load search history from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("searchHistory");
    if (saved) {
      setSearchHistory(JSON.parse(saved));
    }
  }, []);

  const handleSearch = async (query: string) => {
    setIsLoading(true);
    setSearchResult(null);

    try {
      const response = await fetch("http://localhost:8000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setSearchResult(data);

      // Update search history
      const newHistory = [query, ...searchHistory.filter(h => h !== query)].slice(0, 10);
      setSearchHistory(newHistory);
      localStorage.setItem("searchHistory", JSON.stringify(newHistory));

    } catch (error) {
      console.error("Error:", error);
      setSearchResult({
        type: "error",
        response: "Sorry, I encountered an error. Please make sure the backend is running and try again.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleViewDetails = async (productId: string) => {
    try {
      const response = await fetch("http://localhost:8000/product-details", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ product_id: productId }),
      });

      if (response.ok) {
        const data = await response.json();
        setProductDetails(data);
        setSelectedProduct(data.product);
        setShowModal(true);
      }
    } catch (error) {
      console.error("Error fetching product details:", error);
    }
  };

  const handleCompare = (productId: string) => {
    if (compareList.includes(productId)) {
      setCompareList(prev => prev.filter(id => id !== productId));
    } else if (compareList.length < 3) {
      setCompareList(prev => [...prev, productId]);
    }
  };

  const runComparison = async () => {
    if (compareList.length < 2) return;

    setIsLoading(true);
    try {
      const response = await fetch("http://localhost:8000/compare", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ product_ids: compareList }),
      });

      if (response.ok) {
        const data = await response.json();
        setSearchResult({
          type: "comparison_result",
          response: data.response,
          products: data.products,
        });
        setCompareList([]);
      }
    } catch (error) {
      console.error("Error comparing products:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <div className="bg-white border-b shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <ShoppingBag className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">CogniCart</h1>
                <p className="text-sm text-gray-600">AI-Powered Shopping Assistant</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <Badge variant="outline" className="flex items-center gap-1">
                <Brain className="w-3 h-3" />
                Multi-Agent AI
              </Badge>
              {compareList.length > 0 && (
                <Button
                  onClick={runComparison}
                  disabled={compareList.length < 2}
                  variant="outline"
                  className="flex items-center gap-2"
                >
                  <GitCompare className="w-4 h-4" />
                  Compare ({compareList.length})
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Features Banner */}
        {!searchResult && (
          <div className="mb-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <Card className="text-center p-4">
                <Brain className="w-8 h-8 text-blue-600 mx-auto mb-2" />
                <h3 className="font-semibold text-sm">Smart Understanding</h3>
                <p className="text-xs text-gray-600">AI understands your natural language queries</p>
              </Card>
              <Card className="text-center p-4">
                <Award className="w-8 h-8 text-green-600 mx-auto mb-2" />
                <h3 className="font-semibold text-sm">Review Analysis</h3>
                <p className="text-xs text-gray-600">Analyzes thousands of reviews for insights</p>
              </Card>
              <Card className="text-center p-4">
                <TrendingUp className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                <h3 className="font-semibold text-sm">Deal Discovery</h3>
                <p className="text-xs text-gray-600">Finds the best deals and discounts</p>
              </Card>
            </div>
          </div>
        )}

        {/* Search Interface */}
        <div className="mb-8">
          <SearchInterface
            onSearch={handleSearch}
            isLoading={isLoading}
            searchHistory={searchHistory}
          />
        </div>

        {/* Search Results */}
        {searchResult && (
          <div className="space-y-6">
            {/* AI Response */}
            {searchResult.response && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Zap className="w-5 h-5 text-blue-600" />
                    AI Assistant
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="prose max-w-none">
                    <p className="text-gray-700 whitespace-pre-wrap">{searchResult.response}</p>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Product Results */}
            {searchResult.products && searchResult.products.length > 0 && (
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold flex items-center gap-2">
                    <Users className="w-5 h-5 text-gray-600" />
                    Product Recommendations
                  </h2>
                  {searchResult.total_products_found && (
                    <Badge variant="secondary">
                      {searchResult.total_products_found} products found
                    </Badge>
                  )}
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {searchResult.products.map((product) => (
                    <div key={product.id} className="relative">
                      <ProductCard
                        product={product}
                        onViewDetails={handleViewDetails}
                        onCompare={handleCompare}
                      />
                      {compareList.includes(product.id) && (
                        <div className="absolute top-2 right-2">
                          <Badge className="bg-blue-600 text-white">
                            In Compare
                          </Badge>
                        </div>
                      )}
                    </div>
                  ))}
                </div>

                {/* Additional Products */}
                {searchResult.additional_products && searchResult.additional_products.length > 0 && (
                  <div className="mt-8">
                    <h3 className="text-lg font-medium mb-4">More Options</h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      {searchResult.additional_products.slice(0, 8).map((product) => (
                        <ProductCard
                          key={product.id}
                          product={product}
                          onViewDetails={handleViewDetails}
                          onCompare={handleCompare}
                          compact={true}
                        />
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* No Products Found */}
            {searchResult.type === "no_products_found" && (
              <Card>
                <CardContent className="text-center py-8">
                  <ShoppingBag className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No Products Found</h3>
                  <p className="text-gray-600 mb-4">
                    I couldn't find any products matching your criteria. Try refining your search.
                  </p>
                  {searchResult.parsed_query && (
                    <div className="text-left max-w-md mx-auto">
                      <h4 className="font-medium mb-2">Here's what I understood:</h4>
                      <div className="space-y-1 text-sm text-gray-600">
                        {searchResult.parsed_query.product_type && (
                          <p>• Looking for: {searchResult.parsed_query.product_type}</p>
                        )}
                        {searchResult.parsed_query.budget?.max && (
                          <p>• Budget: Under ${searchResult.parsed_query.budget.max}</p>
                        )}
                        {searchResult.parsed_query.features_required?.length > 0 && (
                          <p>• Features: {searchResult.parsed_query.features_required.join(", ")}</p>
                        )}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* Product Details Modal */}
        <ProductDetailsModal
          product={selectedProduct}
          isOpen={showModal}
          onClose={() => setShowModal(false)}
          reviewAnalysis={productDetails?.review_analysis}
          deals={productDetails?.deals}
        />
      </div>
    </div>
  );
}
