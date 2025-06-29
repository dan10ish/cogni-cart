"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Star, ExternalLink, IndianRupee } from "lucide-react";

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

interface ProductResultProps {
  products: Product[];
}

export function ProductResult({ products }: ProductResultProps) {
  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={`w-3 h-3 ${
          i < Math.floor(rating) 
            ? "fill-yellow-400 text-yellow-400" 
            : "text-muted-foreground"
        }`}
      />
    ));
  };

  const handleProductClick = (product: Product) => {
    if (product.url) {
      window.open(product.url, '_blank', 'noopener,noreferrer');
    } else {
      // Fallback to Google search
      const searchQuery = encodeURIComponent(product.title);
      window.open(`https://www.google.com/search?q=${searchQuery}`, '_blank', 'noopener,noreferrer');
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-IN').format(price);
  };

  return (
    <div className="space-y-3">
      {products.map((product) => (
        <Card key={product.id} className="hover:bg-accent/50 transition-colors cursor-pointer group">
          <CardContent className="p-4">
            <div className="flex justify-between items-start gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-start gap-2 mb-2">
                  <h3 className="font-medium line-clamp-2 text-sm group-hover:text-primary transition-colors">
                    {product.title}
                  </h3>
                </div>
                
                <div className="flex items-center gap-2 mb-2">
                  <Badge variant="secondary" className="text-xs px-2 py-0">
                    {product.brand}
                  </Badge>
                  <div className="flex items-center gap-1">
                    {renderStars(product.rating)}
                    <span className="text-xs text-muted-foreground">
                      ({formatPrice(product.review_count)} reviews)
                    </span>
                  </div>
                </div>

                {product.features.length > 0 && (
                  <div className="flex flex-wrap gap-1 mb-2">
                    {product.features.slice(0, 3).map((feature, index) => (
                      <Badge key={index} variant="outline" className="text-xs px-1 py-0">
                        {feature}
                      </Badge>
                    ))}
                    {product.features.length > 3 && (
                      <Badge variant="outline" className="text-xs px-1 py-0">
                        +{product.features.length - 3}
                      </Badge>
                    )}
                  </div>
                )}

                {product.review_summary && product.review_summary !== "No review data available" && product.review_summary !== "Analysis unavailable" && (
                  <p className="text-xs text-muted-foreground line-clamp-2 mb-2">
                    {product.review_summary}
                  </p>
                )}
              </div>

              <div className="flex flex-col items-end gap-2">
                <div className="flex items-center gap-1 text-lg font-semibold">
                  <IndianRupee className="w-4 h-4" />
                  {formatPrice(product.price)}
                </div>
                
                {product.deal_summary && product.deal_summary !== "No deals available" && (
                  <div className="text-xs text-green-600 text-right max-w-24">
                    {product.deal_summary}
                  </div>
                )}

                <Button 
                  size="sm" 
                  variant="outline" 
                  className="text-xs h-7 hover:bg-primary hover:text-primary-foreground transition-colors"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleProductClick(product);
                  }}
                >
                  <ExternalLink className="w-3 h-3 mr-1" />
                  View
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
} 