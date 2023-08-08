export const defaultStyle = (open?: boolean) => ({
    width: '100%',
    overflow: open ? 'visible' : 'hidden',
    transition: 'height ease 0.2s',
});
