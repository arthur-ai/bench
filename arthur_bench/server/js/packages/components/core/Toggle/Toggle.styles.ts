import primary from 'resources/colors/Arthur/primary';

type Props = {
    width: number;
    height: number;
    outlined?: boolean;
    disabled?: boolean;
};

const styles: any = {
    switch: ({ width, height, disabled }: Props) => ({
        position: 'relative',
        display: 'inline-block',
        width: `${width}px`,
        height: `${height}px`,
        ...(disabled && {
            opacity: '0.5',
            pointerEvents: 'none',
        }),
    }),
    slider: ({ width, height, outlined }: Props) => {
        const padding = width > 30 ? 4 : 2;
        return {
            position: 'absolute',
            cursor: 'pointer',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: outlined ? 'transparent' : primary.ashGrey,
            transition: '.4s',
            borderRadius: `${height}px`,
            ...(outlined && {
                boxShadow: `0 0 0 2px ${primary.ashGrey}`,
            }),

            '::before': {
                position: 'absolute',
                content: "''",
                height: `${height - 2 * padding}px`,
                width: `${height - 2 * padding}px`,
                left: `${padding}px`,
                bottom: `${padding}px`,
                backgroundColor: outlined ? primary.purple : 'white',
                transition: '.4s',
                borderRadius: '50%',
            },
        };
    },
    checkbox: ({ width, height, outlined }: Props) => ({
        position: 'absolute',
        opacity: 0,
        width: 0,
        height: 0,

        ':checked + span': {
            backgroundColor: outlined ? 'transparent' : primary.purple,
        },

        ':focus + span': {
            boxShadow: '0 0 1px #2196F3',
        },

        ':checked + span:before': {
            transform: `translateX(${width - height}px)`,
        },
    }),
};

export default styles;
