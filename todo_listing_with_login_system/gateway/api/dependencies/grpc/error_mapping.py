import grpc

grpc_to_http_status = {
    grpc.StatusCode.INVALID_ARGUMENT: 400,
    grpc.StatusCode.PERMISSION_DENIED:403,
    grpc.StatusCode.NOT_FOUND: 404,
    grpc.StatusCode.ALREADY_EXISTS: 409,
    grpc.StatusCode.INTERNAL: 500,
    grpc.StatusCode.UNAVAILABLE: 503,
    grpc.StatusCode.UNKNOWN: 520,
}