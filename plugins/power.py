def run_power():

    power_opts = ['lock', 'logout', 'suspend', 'poweroff', 'reboot', 'hibernate']

    choice = show_menu('power', power_opts)

    if not choice:
        return
    elif choice == 'logout':
        run_cmd('openbox --exit')
    elif choice == 'lock':
        run_cmd('slimlock')
    else:
        run_cmd('systemctl choice')

    return
