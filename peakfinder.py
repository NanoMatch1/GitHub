def find_peaks(dataX, dataY, rangeLow = None, rangeHigh = None, manualPeaks = [], fixedPeaks = [], dataOutput = False, showFig = False, overwrite = False, fileNumber = 0, flipAxis = False ):
    from peakdetect.peakdetect import peakdetect
    from data_processing.data_fit import data_fit
    from data_processing.baseline import baseline_als

    # this will find peaks automatically based on the params "lookahead" and "delta". I believe delta is a gradient cutoff and look ahead is the range over which it checks. Play around to see how it changes
    peaksMax, peaksMin = peakdetect(dataY,dataX,lookahead=2,delta=0.0005)

    # or you can add peaks manually - "peaks" make gaussians, vpeaks is voight type, and lpeaks is lorentzian
    peaks = []

    vpeaks = []
    lpeaks = []
    peaksMax = np.array(peaksMax)
    print(peaksMax)

    plt.plot(peaksMax[:,0],peaksMax[:,1],'o')

    # data = np.transpose([dataX,dataY])
    # this plots a quick baseline using the same "peakdetect" module
    baseline = baseline_als(data[:, 1], 100000, 0.00001)
    dataBaselined = data[:, 1] - baseline
    plt.plot(data[:, 0], data[:, 1])
    plt.plot(data[:, 0], baseline)
    plt.plot(data[:, 0], dataBaselined)
    data = np.column_stack((data[:, 0], dataBaselined))
    print('Data has been baselined')
    plt.show()
    plt.cla()

    # data = data[data[:,0]>1489]
    # data = data[data[:,0]<1800]
    dataYnorm = data[:, 1]-min(data[:, 1])
    dataYnorm = dataYnorm/max(dataYnorm)
    data = np.column_stack((data[:, 0], dataYnorm))
    Fit = data_fit()
    Fit.set_data(data)

    for p in fixedPeaks:
        for m in manualPeaks:
            if p-(0.01*p) <= m <= p+(0.01*p):
                idx = manualPeaks.index(m)
                manualPeaks.pop(idx)

    print('Manual peaks:', manualPeaks)
    print('Fixed peaks:', fixedPeaks)

    # these lines generate the peak fits - first param is peak type, 2nd 3rd and 4th are x position, intensity and FWHM, then the bounds add limitations on those peak fits
    for x in peaks:
        Fit.add_function('gaussian',x, 0.3,5,bounds=[[x*(1-0.005),x*(1+0.005)],[0.05,1],[0.5,15]])

    for x in manualPeaks:
        Fit.add_function('gaussian',x, 0.3,5,bounds=[[x*(1-0.005),x*(1+0.005)],[0.05,1],[0.5,25]])

    for x in lpeaks:
        Fit.add_function('lorentzian',x, 0.3,5,bounds=[[x*(1-0.002),x*(1+0.002)],[0.05,1],[0.5,15]])
    for x in vpeaks:
        Fit.add_function('voigt_pseudo',x, 0.3,5,bounds=[[x*(1-0.002),x*(1+0.002)],[0.05,1],[0.5,15]])
#     Fit.add_function('gaussian',2476, 0.3,5,bounds=[[2476*(1-0.001),2476*(1+0.001)],[0.05,1],[1,20]])


    # here's the magic: it takes all the fitted functions and optimises them within their bounds to get the best fit. This will chug ur PC a little...
    Fit.optimise(maxfev=1000000, ftol=0, gtol=0, xtol=0)

    functions = Fit.get_functions()

    make_dir('{}/output/peakfit'.format(dataDir))
    filename = files[i]
    filename = filename[:-4]
    if dataOutput:
        Fit.save_functions('{}/output/peakfit/{} gauss peakfits-final zoom.csv'.format(dataDir, filename))
    header = headerDict[i]
    if len(header) != 0:
        dataAndHeader = np.vstack((header, data))
    elif len(header) == 0:
        dataAndHeader = data

    plt.plot(data[:, 0], data[:, 1])
    if showFig:
        plt.show()
    if dataOutput:
        np.savetxt('{}/output/peakfit/{} fit data zoom.csv'.format(dataDir, filename), dataAndHeader, delimiter=',', fmt='%s')
    Fit.plot_data(show=False)
    Fit.plot_functions(show=False)
    plt.xlabel('Wavenumber $cm^{-2}$')
    Fit.plot_fit()

    if overwrite == False:
        move_file(files[i], '{}/'.format(dataDir), 'output/peakfit/')




    # fig, axes = plt.subplots()

    # Fit.save_plot('filename')
