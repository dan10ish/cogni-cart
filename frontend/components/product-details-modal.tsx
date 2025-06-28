"use client";

import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Star, TrendingDown, ThumbsUp, ThumbsDown, AlertCircle, CheckCircle, ExternalLink } from "lucide-react";

interface ProductDetailsModalProps {
  product: any;
  isOpen: boolean;
  onClose: () => void;
  reviewAnalysis?: any;
  deals?: any[];
}

export function ProductDetailsModal({ product, isOpen, onClose, reviewAnalysis, deals }: ProductDetailsModalProps) {
  if (!product) return null;

  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={`w-4 h-4 ${
          i < Math.floor(rating) 
            ? "fill-yellow-400 text-yellow-400" 
            : i < rating 
            ? "fill-yellow-200 text-yellow-200" 
            : "text-gray-300"
        }`}
      />
    ));
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-hidden">
        <DialogHeader>
          <DialogTitle className="text-xl font-bold">{product.title}</DialogTitle>
        </DialogHeader>
        
        <ScrollArea className="max-h-[calc(90vh-120px)]">
          <div className="space-y-6">
            {/* Product Header */}
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <Badge variant="secondary">{product.brand}</Badge>
                  <Badge variant="outline">{product.category}</Badge>
                  <Badge variant="outline">{product.availability.replace("_", " ")}</Badge>
                </div>
                
                <div className="flex items-center gap-4 mb-4">
                  <div className="flex items-center gap-1">
                    {renderStars(product.rating)}
                    <span className="text-sm text-gray-600 ml-1">
                      {product.rating} ({product.review_count?.toLocaleString()} reviews)
                    </span>
                  </div>
                  <div className="text-2xl font-bold text-gray-900">
                    ${product.price?.toFixed(2)}
                  </div>
                </div>
              </div>
            </div>

            <Tabs defaultValue="overview" className="w-full">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="reviews">Reviews</TabsTrigger>
                <TabsTrigger value="deals">Deals</TabsTrigger>
                <TabsTrigger value="specs">Specifications</TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="space-y-4">
                {/* Description */}
                <div>
                  <h3 className="font-semibold mb-2">Product Description</h3>
                  <p className="text-gray-700">
                    {product.detailed_description || "A high-quality product designed to meet your needs with excellent features and reliable performance."}
                  </p>
                </div>

                {/* Key Features */}
                <div>
                  <h3 className="font-semibold mb-2">Key Features</h3>
                  <div className="grid grid-cols-2 gap-2">
                    {product.features?.map((feature: string, index: number) => (
                      <div key={index} className="flex items-center gap-2">
                        <CheckCircle className="w-4 h-4 text-green-600" />
                        <span className="text-sm">{feature}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Pros and Cons */}
                {(product.pros || product.cons) && (
                  <div className="grid grid-cols-2 gap-4">
                    {product.pros && (
                      <div>
                        <h3 className="font-semibold mb-2 text-green-700">Pros</h3>
                        <ul className="space-y-1">
                          {product.pros.map((pro: string, index: number) => (
                            <li key={index} className="flex items-start gap-2">
                              <ThumbsUp className="w-3 h-3 text-green-600 mt-0.5" />
                              <span className="text-sm">{pro}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    
                    {product.cons && (
                      <div>
                        <h3 className="font-semibold mb-2 text-red-700">Cons</h3>
                        <ul className="space-y-1">
                          {product.cons.map((con: string, index: number) => (
                            <li key={index} className="flex items-start gap-2">
                              <ThumbsDown className="w-3 h-3 text-red-600 mt-0.5" />
                              <span className="text-sm">{con}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}

                {/* Best For */}
                {product.best_for && (
                  <div>
                    <h3 className="font-semibold mb-2">Best For</h3>
                    <div className="flex flex-wrap gap-2">
                      {product.best_for.map((useCase: string, index: number) => (
                        <Badge key={index} variant="outline">{useCase}</Badge>
                      ))}
                    </div>
                  </div>
                )}
              </TabsContent>

              <TabsContent value="reviews" className="space-y-4">
                {reviewAnalysis ? (
                  <div>
                    <div className="grid grid-cols-3 gap-4 mb-6">
                      <div className="text-center p-4 bg-green-50 rounded-lg">
                        <div className="text-2xl font-bold text-green-700">
                          {reviewAnalysis.sentiment_breakdown?.positive_percentage || 0}%
                        </div>
                        <div className="text-sm text-green-600">Positive</div>
                      </div>
                      <div className="text-center p-4 bg-yellow-50 rounded-lg">
                        <div className="text-2xl font-bold text-yellow-700">
                          {reviewAnalysis.sentiment_breakdown?.neutral_percentage || 0}%
                        </div>
                        <div className="text-sm text-yellow-600">Neutral</div>
                      </div>
                      <div className="text-center p-4 bg-red-50 rounded-lg">
                        <div className="text-2xl font-bold text-red-700">
                          {reviewAnalysis.sentiment_breakdown?.negative_percentage || 0}%
                        </div>
                        <div className="text-sm text-red-600">Negative</div>
                      </div>
                    </div>

                    <div className="space-y-4">
                      {/* Common Praises */}
                      {reviewAnalysis.common_praises && (
                        <div>
                          <h3 className="font-semibold mb-2 text-green-700">What Customers Love</h3>
                          <ul className="space-y-1">
                            {reviewAnalysis.common_praises.map((praise: string, index: number) => (
                              <li key={index} className="flex items-start gap-2">
                                <ThumbsUp className="w-3 h-3 text-green-600 mt-0.5" />
                                <span className="text-sm">{praise}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Common Complaints */}
                      {reviewAnalysis.common_complaints && (
                        <div>
                          <h3 className="font-semibold mb-2 text-red-700">Common Issues</h3>
                          <ul className="space-y-1">
                            {reviewAnalysis.common_complaints.map((complaint: string, index: number) => (
                              <li key={index} className="flex items-start gap-2">
                                <ThumbsDown className="w-3 h-3 text-red-600 mt-0.5" />
                                <span className="text-sm">{complaint}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Red Flags */}
                      {reviewAnalysis.red_flags && reviewAnalysis.red_flags.length > 0 && (
                        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                          <h3 className="font-semibold mb-2 text-red-700 flex items-center gap-2">
                            <AlertCircle className="w-4 h-4" />
                            Important Considerations
                          </h3>
                          <ul className="space-y-1">
                            {reviewAnalysis.red_flags.map((flag: string, index: number) => (
                              <li key={index} className="text-sm text-red-700">• {flag}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                ) : (
                  <div className="text-center text-gray-500 py-8">
                    Review analysis not available for this product.
                  </div>
                )}
              </TabsContent>

              <TabsContent value="deals" className="space-y-4">
                {deals && deals.length > 0 ? (
                  <div className="space-y-4">
                    {deals.map((deal, index) => (
                      <div key={index} className="p-4 bg-green-50 border border-green-200 rounded-lg">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h3 className="font-semibold text-green-800">{deal.title}</h3>
                            <p className="text-sm text-green-700 mt-1">{deal.description}</p>
                            
                            <div className="flex items-center gap-4 mt-2">
                              <div className="text-lg font-bold text-green-900">
                                Save ${deal.savings?.toFixed(2)}
                              </div>
                              {deal.coupon_code && (
                                <Badge variant="outline" className="bg-white">
                                  Code: {deal.coupon_code}
                                </Badge>
                              )}
                            </div>
                            
                            <div className="text-xs text-green-600 mt-1">
                              Valid until: {deal.valid_until} • {deal.retailer}
                            </div>
                          </div>
                          
                          <TrendingDown className="w-5 h-5 text-green-600" />
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center text-gray-500 py-8">
                    No current deals available for this product.
                  </div>
                )}
              </TabsContent>

              <TabsContent value="specs" className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <h3 className="font-semibold mb-2">Basic Information</h3>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-600">Brand:</span>
                        <span className="text-sm font-medium">{product.brand}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-600">Category:</span>
                        <span className="text-sm font-medium">{product.category}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-600">Type:</span>
                        <span className="text-sm font-medium">{product.product_type}</span>
                      </div>
                      {product.weight && (
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Weight:</span>
                          <span className="text-sm font-medium">{product.weight}</span>
                        </div>
                      )}
                    </div>
                  </div>
                  
                  {product.key_specifications && (
                    <div>
                      <h3 className="font-semibold mb-2">Specifications</h3>
                      <div className="space-y-2">
                        {Object.entries(product.key_specifications).map(([key, value]: [string, any]) => (
                          <div key={key} className="flex justify-between">
                            <span className="text-sm text-gray-600">{key}:</span>
                            <span className="text-sm font-medium">{value}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </TabsContent>
            </Tabs>
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
} 