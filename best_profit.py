class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """
        Purpose: Returns the highest profit you can make 
        by buying and selling stock, at most once.

        Note: Scans graph from left to right, updating global max and min.

        """
        lowest = float('inf')
        highest = float('-inf')
        profit = 0
        for p in reversed(prices):
            if p > highest:
                highest = p
                lowest = float('inf')
                
            elif p <= highest:
                if p < lowest:
                    lowest = p
                    if highest - lowest > profit:
                        profit = highest - lowest
        return profit


    def maxProfit(self, prices: List[int]) -> int:
        """Updated solver.
        """
        max_profit, min_price = 0, float('inf')
        for x in prices:
            min_price = min(min_price, x) # ensures min price is BEFORE x
            profit = x - min_price
            max_profit = max(max_profit, profit) # calculates largest profit
            
        return max_profit


    def maxProfitII(self, prices: List[int]) -> int:
        """
        Purpose: Returns max. profit you can achieve, when you can complete as 
        many transactions as you like. 

        Note: You cannot engage in multiple transactions simultaneously.
        """
        res = 0
        
        for i in range(1, len(prices)):
            if prices[i] > prices[i-1]:
                res += (prices[i] - prices[i-1])
                
        return res