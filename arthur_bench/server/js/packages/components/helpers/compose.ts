export const compose =
    (...functions: any) =>
    (args: any) =>
        functions.reduceRight((arg: any, fn: any) => fn(arg), args);
