export const exists = <T>(value: T) => value !== undefined && value !== null;

export const getKey: any = (keys: Array<string>, obj: Record<any, any>) =>
    obj && keys.length ? getKey(keys.slice(1), obj[keys[0]]) : obj;

export const get =
    (key: string, fallback?: string | number | null) => (obj: any) => {
        const keys = String(key).split('.');
        if (!exists(obj)) {
            return fallback;
        }
        const result = getKey(keys, obj);

        return result === undefined ? fallback : result;
    };
