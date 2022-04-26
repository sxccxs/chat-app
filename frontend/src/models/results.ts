export type Result<E> = {
    isSuccess: true
} | {
    isSuccess: false,
    exception: E
}

export type VResult<T, E> = {
    isSuccess: true,
    value: T
} | {
    isSuccess: false,
    exception: E
}

