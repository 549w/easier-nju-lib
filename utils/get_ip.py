from fastapi import Request

def get_client_ip(request: Request) -> str:
    # 常见代理头
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        # 可能是多个 IP：client, proxy1, proxy2
        return x_forwarded_for.split(",")[0].strip()

    x_real_ip = request.headers.get("x-real-ip")
    if x_real_ip:
        return x_real_ip

    # fallback
    if request.client:
        return request.client.host
    return "unknown_ip"