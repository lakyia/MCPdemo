import requests
import akshare as ak
import uvicorn
from fastmcp.server import FastMCP

# Create server
mcp = FastMCP("Echo Server")



@mcp.tool()
def get_current_weather(city: str) -> str:
    """Get the current weather for a city"""
    print(f"[debug-server] get_current_weather({city})")

    endpoint = "https://uapis.cn/api/v1/misc/weather?city="
    full_url = f"{endpoint}{city}"
    print(f"[debug-server] 请求天气 API: {full_url}")
    
    try:
        response = requests.get(full_url)
        print(f"[debug-server] 响应状态码: {response.status_code}")
        print(f"[debug-server] 响应内容: {response.text}")
        return response.text
    except Exception as e:
        print(f"[debug-server] 请求错误: {str(e)}")
        return f"{str(e)}"


@mcp.tool()
def get_num_rand(num: int) -> str:
    """Get a random multiple of the given number"""
    import random
    print(f"[debug-server] get_num_rand({num})")
    
    # Generate a random multiple between 1 and 10
    random_multiplier = random.randint(1, 10)
    result = num * random_multiplier
    print(f"[debug-server] Random multiplier: {random_multiplier}, Result: {result}")
    
    return f"{result}"


@mcp.tool()
def get_stock_quote(symbol: str) -> str:
    """Get stock bid and ask quotes from East Money"""
    print(f"[debug-server] get_stock_quote({symbol})")
    
    try:
        # Get stock bid and ask data
        stock_bid_ask_em_df = ak.stock_bid_ask_em(symbol=symbol)
        print(f"[debug-server] Stock data retrieved successfully for {symbol}")
        print(f"[debug-server] Data shape: {stock_bid_ask_em_df.shape}")
        print(f"[debug-server] Data head:\n{stock_bid_ask_em_df.head()}")
        
        # Convert DataFrame to JSON
        result = stock_bid_ask_em_df.to_json(orient="records", force_ascii=False)
        print(f"[debug-server] Result JSON: {result[:100]}...")
        
        return result
    except Exception as e:
        print(f"[debug-server] Error getting stock data: {str(e)}")
        return f"Error: {str(e)}"

sse_app = mcp.http_app(transport="sse")
def main():
    uvicorn.run(sse_app, host="0.0.0.0", port=8000,debug=True)
if __name__ == "__main__":
    main()
   
