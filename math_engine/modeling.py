import os
import os.path
import numpy as np
import pandas as pd
import numpy.linalg as npla
import plotly.graph_objs as go
import plotly.offline
from plotly import subplots
from  scipy import ndimage# import scipy


class MultiDimensionalModeling():
    def __init__(self):
        self.maintenance_by_sn = 'level tank 02'
        self.pareto = 0.99  # 0.99999999 # 1 #0.85 #1 #
        self.sm_window = 50 #2 #1 #5 #
        self.hlh_prcnt = 100 #99.99 #95 #85 #
        self.ylw = 1.2
        self.red = 1.5
        self.trn_plt = 1
        self.tst_plt = 1
        self.show_plots = True

    def training_handler(self, X, y, extend_degree): #
        # this function performs linear regression for possibly extended explanatory variables
        X_ext = self.extend_n_degree(X.copy(), extend_degree)
        y_column_name = y.columns[0]
        if extend_degree > 1:
            # implement pca
            regeig, regres = self.pca(X_ext, self.pareto)
        else:
            regres = X_ext
            regeig = []
        XTX = regres.transpose().dot(regres)
        my_inv = npla.inv(XTX)
        pseudo_inverse = my_inv.dot(regres.transpose())
        coeffs = pseudo_inverse.dot(y)
        # compare results to existing library - in GMail
        # regr = linear_model.LinearRegression()
        # regr.fit(regres, y)
        y_est = pd.DataFrame(index = y.index, columns = y.columns)
        y_est = regres.dot(coeffs)
        y_est.columns = [y_column_name]
        errors = pd.DataFrame(index = y.index, columns = y.columns)
        errors = np.abs(y[y_column_name] - y_est[y_column_name])
        sm_window = self.sm_window
        # sm_errors = np.empty((len(errors),))
        # sm_errors[:] = np.nan
        # for sn in range(sm_window, len(errors)):
        #     sm_errors[sn] = np.min(errors[sn - sm_window:sn])
        if (y.std().values > 0):
            R_2 = 1 - errors.var()/ y.var()
        else:
            R_2 = []
        sm_window = self.sm_window
        sm_errors = ndimage.filters.minimum_filter1d(errors, self.sm_window, axis=0)
        residuals = sm_errors
        residuals[0:sm_window - 1] = 0
        results_df = pd.DataFrame(index=errors.index, columns=['y', 'y_est', 'residuals'])
        residuals_df = pd.DataFrame(data=residuals, index=errors.index, columns=['ActValue'])
        hlh = np.percentile(residuals[sm_window:len(residuals)], self.hlh_prcnt)
        ylw_thr = hlh * self.ylw
        red_thr = hlh * self.red
        trn_struct = trn_class(coeffs, X, y, y_est, errors, sm_errors, residuals_df, regeig, regres, R_2, hlh, ylw_thr, red_thr, extend_degree)
        return trn_struct

    def pca(self, ext_X, pareto):
        # compute principal components of the data and take the important onces only
        XTX = ext_X.transpose().dot(ext_X)
        [eigval, eigvec] = npla.eig(XTX)
        eigvec = abs(eigvec)
        eigval = abs(eigval)
        weights = np.cumsum(eigval) / np.sum(eigval)
        regind = np.where(weights < pareto)[0]
        if len(regind) > 0:
            regeig = eigvec[:, regind]
        else:
            regeig = eigvec[:, list(range(2))]
        regres = ext_X.dot(regeig)
        return regeig, regres



    def plot_model_phase(self, phase_struct, refer_struct, modelID, explained_ID, explanatory_cptn, extend_degree, fname, plot_dir):
        # plot modeling results
        explained_cptn = explained_ID
        phase_struct.y.index = pd.to_datetime(phase_struct.y.index).strftime('%r')
        real = go.Scatter(x=phase_struct.y.index, y=phase_struct.y[explained_ID[0]] , mode ='markers', name='Explained_real: %s' % explained_cptn, marker = dict(size = 5, color ='blue'), line = dict(width = 2, color ='blue'))#(x=trn_ind, y=trn_struct.y[:, 0])
        estimated = go.Scatter(x=phase_struct.y.index, y=list(phase_struct.y_est[explained_ID[0]]), mode ='markers', name='Explained_estimated: %s' % explained_cptn, marker = dict(size = 5, color ='green'), line = dict(width = 2, color ='green'))#(x=trn_ind, y=trn_struct.y_est[:, 0])
        residuals = go.Scatter(x=phase_struct.y.index, y=list(phase_struct.residuals_df['ActValue']), mode ='markers', name='Residuals', marker = dict(size = 5, color ='black'), line = dict(width = 2, color ='black'))#(x=trn_ind, y=trn_struct.sm_errors)
        ylw_threshold = go.Scatter(x=phase_struct.y.index, y=np.ones((len(phase_struct.y.index))) * refer_struct.ylw_thr, mode = 'lines', name='Defect was detected', line = dict(width = 2, color = 'yellow'))#(x=trn_ind, y=trn_struct.sm_errors)
        red_threshold = go.Scatter(x=phase_struct.y.index, y=np.ones((len(phase_struct.y.index))) * refer_struct.red_thr, mode = 'lines', name='Existing failure was detected', line = dict(width = 2, color = 'red'))#(x=trn_ind, y=trn_struct.sm_errors)

        vline_strt_explained = go.Scatter(
            # x=[separating_line, separating_line],
            x=[phase_struct.y.index[0], phase_struct.y.index[0]],
            y=[np.min(phase_struct.y_est), np.max(phase_struct.y_est)], mode='lines+markers',
            line=dict(shape='linear'),
            showlegend=False)
        vline_end_explained = go.Scatter(
            # x=[separating_line, separating_line],
            # x=[phase_struct.y.index[refer_struct.X.shape[0] - 1], phase_struct.y.index[refer_struct.X.shape[0] - 1]],
            x=[phase_struct.y.index[-1], phase_struct.y.index[-1]],
            y=[np.min(phase_struct.y_est), np.max(phase_struct.y_est)], mode='lines+markers',
            line=dict(shape='linear'),
            showlegend=False)
        vline_strt_residuals = go.Scatter(
            # x=[separating_line, separating_line], # [phase_struct.y.index[refer_struct.X.shape[0] - 1], phase_struct.y.index[refer_struct.X.shape[0] - 1]],
            x=[phase_struct.y.index[0], phase_struct.y.index[0]],
            y=[np.min(phase_struct.residuals_df), np.max(phase_struct.residuals_df)], mode='lines+markers',
            line=dict(shape='linear'),
            showlegend=False)
        vline_end_residuals = go.Scatter(
            # x=[separating_line, separating_line], # [phase_struct.y.index[refer_struct.X.shape[0] - 1], phase_struct.y.index[refer_struct.X.shape[0] - 1]],
            # x=[phase_struct.y.index[refer_struct.X.shape[0] - 1], phase_struct.y.index[refer_struct.X.shape[0] - 1]],
            x=[phase_struct.y.index[-1], phase_struct.y.index[-1]],
            y=[np.min(phase_struct.residuals_df), np.max(phase_struct.residuals_df)], mode='lines+markers',
            line=dict(shape='linear'),
            showlegend=False)
        # vertical line that separates phases
        if ('trn-tst' in fname):
            separating_line = refer_struct.y.index.max()
            vline_explained = go.Scatter(
                x=[separating_line, separating_line],
                y=[np.min(phase_struct.y_est), np.max(phase_struct.y_est)], mode='lines+markers', name='trn size',
                line=dict(shape='linear'),
                showlegend=False)
            vline_residuals = go.Scatter(
                x=[separating_line, separating_line], # [phase_struct.y.index[refer_struct.X.shape[0] - 1], phase_struct.y.index[refer_struct.X.shape[0] - 1]],
                y=[np.min(phase_struct.residuals_df), np.max(phase_struct.residuals_df)], mode='lines+markers', name='trn size',
                line=dict(shape='linear'),
                showlegend=False)
        N_subplots = 2 + 1 + len(explanatory_cptn)

        ttl_str = (('Values of explained variable'), )
        ttl_str = ttl_str + (('Residuals'), )
        # find original number of variables (before extension)
        org_var_num = len(explanatory_cptn)
        for explanatory_sn in range(org_var_num):
             ttl_str = ttl_str + ('Values of %s' % (explanatory_cptn[explanatory_sn]), )
        ttl_str = tuple(ttl_str)

        fig = subplots.make_subplots(rows=org_var_num + 2 , cols=1, subplot_titles=(ttl_str), print_grid=False) #
        # fig, axes = plt.subplots(nrows=len(months.unique()), ncols=1, sharex='all', sharey='all')

        fig.append_trace(real, 1, 1)
        fig.append_trace(estimated, 1, 1)
        fig.append_trace(residuals, 2, 1)
        fig.append_trace(ylw_threshold, 2, 1)
        fig.append_trace(red_threshold, 2, 1)
        fig.append_trace(vline_strt_explained, 1, 1)
        fig.append_trace(vline_strt_residuals, 2, 1)
        fig.append_trace(vline_end_explained, 1, 1)
        fig.append_trace(vline_end_residuals, 2, 1)
        if ('trn-tst' in fname):
            fig.append_trace(vline_explained, 1, 1)
            fig.append_trace(vline_residuals, 2, 1)
        subplot_sn = 3
        # fig.append_trace(real, subplot_sn, 1)
        # subplot_sn = subplot_sn + 1
        for col in range(org_var_num):
            phase_struct.X.index = pd.to_datetime(phase_struct.X.index).strftime('%r')
            explanatory_sig = go.Scatter(x=phase_struct.X.index, y=list(phase_struct.X[explanatory_cptn[subplot_sn - 3]]), mode ='markers', name='Explanatory %s' % explanatory_cptn[col], marker = dict(size = 5, color ='blue'), line = dict(width = 2, color ='blue'))
            vline_strt = go.Scatter(
                x=[phase_struct.y.index[0], phase_struct.y.index[0]],
                y=[np.min(phase_struct.X[explanatory_cptn[subplot_sn - 3]]), np.max(phase_struct.X[explanatory_cptn[subplot_sn - 3]])], mode='lines+markers',
                line=dict(shape='linear'),
                showlegend=False)
            vline_end = go.Scatter(
                x=[phase_struct.y.index[-1], phase_struct.y.index[-1]],
                y=[np.min(phase_struct.X[explanatory_cptn[subplot_sn - 3]]), np.max(phase_struct.X[explanatory_cptn[subplot_sn - 3]])], mode='lines+markers',
                line=dict(shape='linear'),
                showlegend=False)
            fig.append_trace(explanatory_sig, subplot_sn, 1)
            fig.append_trace(vline_strt, subplot_sn, 1)
            fig.append_trace(vline_end, subplot_sn, 1)
            subplot_sn = subplot_sn + 1

        fig['layout'].update(height=400 * (org_var_num + 2), width=2000, title='Diagnostics of %s, R_2 is %f' % (modelID, refer_struct.R_2)) #, layout=layout

        if not os.path.exists(plot_dir):
            os.mkdir(plot_dir)
        # plotly.offline.plot(fig, filename = '%s%s_%s' % (plot_dir, modelID, fname), auto_open=True) #
        filename_for_plot = '%s%s_%s.html' % (plot_dir, modelID, fname)
        # if filename exists - delete for  in phase_struct:
        plotly.offline.plot(fig, filename = filename_for_plot , auto_open=self.show_plots)  #
        print('\t%s was finished' % fname)

    def testing_handler(self, X, y, trn, extend_degree):
        # extend and rotate a new batch of record as it was done in training, substite the results to the polynomeal from traing and compare Y real and Y estimated
        X_ext = self.extend_n_degree(X, extend_degree)
        y_column_name = y.columns[0]
        if extend_degree > 1:
            # implement pca
            regress = X_ext.dot(trn.regeig)
        else:
            regress = X_ext
        y_est = pd.DataFrame(index = y.index, columns = y.columns)
        y_est = regress.dot(trn.coeffs)
        y_est.columns = [y_column_name]
        errors = abs(y_est - y)
        sm_window = self.sm_window
        sm_errors = ndimage.filters.minimum_filter1d(errors, self.sm_window, axis=0)
        # sm_errors = errors.copy()
        # sm_errors[:] = np.nan
        # for sn in range(sm_window, len(errors)):
        #     sm_errors[sn] = np.min(errors[sn - sm_window:sn])
        residuals = sm_errors
        residuals[0:sm_window - 1] = 0
        results_df = pd.DataFrame(index=errors.index, columns=['y', 'y_est', 'residuals'])
        residuals_df = pd.DataFrame(data = residuals, index=errors.index, columns=['ActValue'])
        grnind = np.where((0 <= residuals[sm_window:]) & (residuals[sm_window:] < trn.ylw_thr))[0]
        ylwind = np.where((residuals[sm_window:] >= trn.ylw_thr) & (residuals[sm_window:] < trn.red_thr))[0]
        redind = np.where(residuals[sm_window:] >= trn.red_thr)[0]

        decision = np.zeros(np.shape(residuals))
        decision[grnind] = 0
        decision[ylwind] = 1
        decision[redind] = 2

        tst_struct = tst_class(X, y, y_est, errors, sm_errors, residuals_df, decision)
        # tst_file = open('%s\\tst_struct.py' % self.plot_dir,  "wb")
        # pickle.dump(tst_struct, tst_file, pickle.HIGHEST_PROTOCOL)
        # tst_file.close()
        return tst_struct

    def extend_n_degree(self, X, extend_degree):
        assert extend_degree < 4
        cptn = X.columns
        X_len = X.shape[0]
        X_width = X.shape[1]
        last_column = 0
        if extend_degree >= 1:
            ext_X = X.copy()
            last_column = X_width

        if extend_degree >= 2:
            for col1 in range(X_width):
                for col2 in range(col1, X_width):
                    last_column = last_column + 1
                    add_cptn = '%s*%s' % (str(cptn[col1]), str(cptn[col2]))
                    X[add_cptn] = X[cptn[col1]] * X[cptn[col2]]
                    # add_cptn[last_column] = str(cptn[col1]) + '*' + str(cptn[col2])
                    # ext_X = np.concatenate((ext_X, add_col), axis=1)

        if extend_degree >= 3:
            for col1 in range(X_width):
                for col2 in range(col1, X_width):
                    for col3 in range(col2, X_width):
                        # last_column = last_column + 1
                        add_cptn = '%s*%s*%s' % (str(cptn[col1]), str(cptn[col2]), str(cptn[col3]))
                        X[add_cptn] = X[cptn[col1]] * X[cptn[col2]] * X[cptn[col3]]
                        # add_cptn[last_column] = str(cptn[col1]) + '*' + str(cptn[col2]) + '*' + str(cptn[col3])
                        # ext_X = np.concatenate((ext_X, add_col), axis=1)

        X_ext = X
        return X_ext

class trn_class():
    # class for saving trn_results
    def __init__(self, coeffs, X, y, y_est, errors, sm_errors, residuals_df, regeig, regres, R_2, hlh, ylw_thr, red_thr, extend_degree):
        self.coeffs = coeffs
        self.X = X
        self.y = y
        self.y_est = y_est
        self.errors = errors
        self.sm_errors = sm_errors
        self.residuals_df = residuals_df
        self.regeig = regeig
        self.regres = regres
        self.R_2 = R_2
        self.hlh = hlh
        self.ylw_thr = ylw_thr
        self.red_thr = red_thr
        self.extend_degree = extend_degree

class tst_class():
    # class for saving tst_results
    def __init__(self, X, y, y_est, errors, sm_errors, residuals_df, decision):
        self.X = X
        self.y = y
        self.y_est = y_est
        self.errors = errors
        self.sm_errors = sm_errors
        self.residuals_df = residuals_df
        self.decision = decision


