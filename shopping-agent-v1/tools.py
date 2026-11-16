from langchain.tools import tool


@tool
def get_price(product_name:str) -> str:
    """获取商品价格 a是商品名称
      查询商品的模拟单价。
    a 是商品名称，目前仅支持：笔记本（纸质）、钢笔、书、橡皮 。
    不支持手机、电脑或其他商品，也不能查询实时价格。
    """
    print(f"执行 get_price：{product_name}")
    prices = {
        "笔记本": 12,
        "钢笔": 8,
        "书": 30,
        "橡皮": 1
    }
    if product_name in prices:
        return str(prices[product_name])
    else:
        raise ValueError(f"没有「{product_name}」的价格，无法计算它的总价。")

@tool
def calculate_total(prices:float,quantity:int) -> str:
    """计算总价 prices是商品价格列表，b是数量"""
    print(f"执行 calculate_total：{prices} * {quantity}")
    if quantity <= 0:
        return "计算失败：购买数量必须大于 0。"
    return str(prices * quantity)

@tool
def sum_totals(amounts: list[float]) -> str:
    """将多个商品的小计相加，amounts 是小计金额列表。"""
    print(f"执行 sum_totals：{amounts}")

    return str(sum(amounts))
