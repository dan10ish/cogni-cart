"use client";

import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Star, ShoppingCart, Eye, TrendingUp, TrendingDown } from "lucide-react";

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

interface ProductCardProps {
  product: Product;
  onViewDetails: (productId: string) => void;
  onCompare?: (productId: string) => void;
  compact?: boolean;
}

export function ProductCard({ product, onViewDetails, onCompare, compact = false }: ProductCardProps) {
  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={`w-3 h-3 ${
          i < Math.floor(rating) 
            ? "fill-yellow-400 text-yellow-400" 
            : i < rating 
            ? "fill-yellow-200 text-yellow-200" 
            : "text-gray-300"
        }`}
      />
    ));
  };

  const getAvailabilityColor = (availability: string) => {
    switch (availability) {
      case "in_stock": return "bg-green-100 text-green-800";
      case "limited_stock": return "bg-yellow-100 text-yellow-800";
      case "out_of_stock": return "bg-red-100 text-red-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <Card className={`w-full ${compact ? "h-auto" : "h-[400px]"} hover:shadow-lg transition-shadow`}>
      <CardHeader className="pb-2">
        <div className="flex justify-between items-start">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <Badge variant="secondary" className="text-xs">
                {product.brand}
              </Badge>
              <Badge 
                className={`text-xs ${getAvailabilityColor(product.availability)}`}
                variant="outline"
              >
                {product.availability.replace("_", " ")}
              </Badge>
            </div>
            <h3 className={`font-semibold ${compact ? "text-sm" : "text-base"} line-clamp-2 text-gray-900`}>
              {product.title}
            </h3>
          </div>
        </div>
        
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-1">
            {renderStars(product.rating)}
            <span className="text-sm text-gray-600 ml-1">
              ({product.review_count.toLocaleString()})
            </span>
          </div>
          <div className="text-right">
            <div className="text-lg font-bold text-gray-900">
              ${product.price.toFixed(2)}
            </div>
          </div>
        </div>
      </CardHeader>

      <CardContent className="pt-0">
        {/* Deal Summary */}
        {product.deal_summary && product.deal_summary !== "No deals available" && (
          <div className="mb-3 p-2 bg-green-50 border border-green-200 rounded-md">
            <div className="flex items-center gap-1">
              <TrendingDown className="w-3 h-3 text-green-600" />
              <span className="text-xs text-green-700 font-medium">
                {product.deal_summary}
              </span>
            </div>
          </div>
        )}

        {/* Features */}
        <div className="mb-3">
          <div className="flex flex-wrap gap-1">
            {product.features.slice(0, compact ? 2 : 3).map((feature, index) => (
              <Badge key={index} variant="outline" className="text-xs py-0 px-1">
                {feature}
              </Badge>
            ))}
            {product.features.length > (compact ? 2 : 3) && (
              <Badge variant="outline" className="text-xs py-0 px-1">
                +{product.features.length - (compact ? 2 : 3)} more
              </Badge>
            )}
          </div>
        </div>

        {/* Review Summary */}
        {product.review_summary && product.review_summary !== "No review data available" && !compact && (
          <div className="mb-3 text-xs text-gray-600 line-clamp-2">
            {product.review_summary}
          </div>
        )}

        {/* Action Buttons */}
        <div className={`flex gap-2 ${compact ? "mt-2" : "mt-auto"}`}>
          <Button 
            onClick={() => onViewDetails(product.id)}
            className="flex-1 text-xs h-8"
            variant="default"
          >
            <Eye className="w-3 h-3 mr-1" />
            Details
          </Button>
          {onCompare && (
            <Button 
              onClick={() => onCompare(product.id)}
              variant="outline"
              className="text-xs h-8 px-2"
            >
              Compare
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
} 