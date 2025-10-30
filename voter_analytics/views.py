# File: views.py
# Author: Travis Falk(travisf@bu.edu), 10/29/2025
# Description: View definitions for voter_analytics app

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter

# imports for plotly
import plotly
import plotly.graph_objs as go

# Create your views here.

class VoterListView(ListView):
    """View to display voter records."""
    
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100
    
    def get_queryset(self):
        """Filter voters based on search criteria."""
        
        # start with entire queryset
        qs = super().get_queryset()
        
        # filter by party affiliation
        if 'party_affiliation' in self.request.GET:
            party = self.request.GET['party_affiliation']
            if party:
                qs = qs.filter(party_affiliation=party)
        
        # filter by minimum birth year
        if 'min_birth_year' in self.request.GET:
            min_year = self.request.GET['min_birth_year']
            if min_year:
                qs = qs.filter(date_of_birth__year__gte=min_year)
        
        # filter by maximum birth year
        if 'max_birth_year' in self.request.GET:
            max_year = self.request.GET['max_birth_year']
            if max_year:
                qs = qs.filter(date_of_birth__year__lte=max_year)
        
        # filter by voter score
        if 'voter_score' in self.request.GET:
            score = self.request.GET['voter_score']
            if score:
                qs = qs.filter(voter_score=score)
        
        # filter by participation in 2020 state election
        if 'v20state' in self.request.GET:
            qs = qs.filter(v20state=True)
        
        # filter by participation in 2021 town election
        if 'v21town' in self.request.GET:
            qs = qs.filter(v21town=True)
        
        # filter by participation in 2021 primary
        if 'v21primary' in self.request.GET:
            qs = qs.filter(v21primary=True)
        
        # filter by participation in 2022 general election
        if 'v22general' in self.request.GET:
            qs = qs.filter(v22general=True)
        
        # filter by participation in 2023 town election
        if 'v23town' in self.request.GET:
            qs = qs.filter(v23town=True)
        
        return qs


class VoterDetailView(DetailView):
    """View to show detail page for one voter."""
    
    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'voter'


class GraphsView(ListView):
    """View to display graphs of voter data."""
    
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'
    
    def get_queryset(self):
        """Filter voters based on search criteria."""
        
        # start with entire queryset
        qs = super().get_queryset()
        
        # filter by party affiliation
        if 'party_affiliation' in self.request.GET:
            party = self.request.GET['party_affiliation']
            if party:
                qs = qs.filter(party_affiliation=party)
        
        # filter by minimum birth year
        if 'min_birth_year' in self.request.GET:
            min_year = self.request.GET['min_birth_year']
            if min_year:
                qs = qs.filter(date_of_birth__year__gte=min_year)
        
        # filter by maximum birth year
        if 'max_birth_year' in self.request.GET:
            max_year = self.request.GET['max_birth_year']
            if max_year:
                qs = qs.filter(date_of_birth__year__lte=max_year)
        
        # filter by voter score
        if 'voter_score' in self.request.GET:
            score = self.request.GET['voter_score']
            if score:
                qs = qs.filter(voter_score=score)
        
        # filter by participation in 2020 state election
        if 'v20state' in self.request.GET:
            qs = qs.filter(v20state=True)
        
        # filter by participation in 2021 town election
        if 'v21town' in self.request.GET:
            qs = qs.filter(v21town=True)
        
        # filter by participation in 2021 primary
        if 'v21primary' in self.request.GET:
            qs = qs.filter(v21primary=True)
        
        # filter by participation in 2022 general election
        if 'v22general' in self.request.GET:
            qs = qs.filter(v22general=True)
        
        # filter by participation in 2023 town election
        if 'v23town' in self.request.GET:
            qs = qs.filter(v23town=True)
        
        return qs
    
    def get_context_data(self, **kwargs):
        """Provide context variables for use in template."""
        
        # start with superclass context
        context = super().get_context_data(**kwargs)
        voters = context['voters']
        
        # Graph 1: Histogram of birth years
        birth_years = [v.date_of_birth.year for v in voters]
        year_counts = {}
        for year in birth_years:
            year_counts[year] = year_counts.get(year, 0) + 1
        
        x1 = sorted(year_counts.keys())
        y1 = [year_counts[year] for year in x1]
        
        fig1 = go.Bar(x=x1, y=y1)
        title_text1 = "Voter Distribution by Year of Birth"
        graph_div_birth_year = plotly.offline.plot(
            {"data": [fig1], "layout_title_text": title_text1},
            auto_open=False,
            output_type="div"
        )
        context['graph_div_birth_year'] = graph_div_birth_year
        
        # Graph 2: Pie chart of party affiliation
        party_counts = {}
        for v in voters:
            party = v.party_affiliation.strip()
            party_counts[party] = party_counts.get(party, 0) + 1
        
        x2 = list(party_counts.keys())
        y2 = list(party_counts.values())
        
        fig2 = go.Pie(labels=x2, values=y2)
        title_text2 = "Voter Distribution by Party Affiliation"
        graph_div_party = plotly.offline.plot(
            {"data": [fig2], "layout_title_text": title_text2},
            auto_open=False,
            output_type="div"
        )
        context['graph_div_party'] = graph_div_party
        
        # Graph 3: Histogram of election participation
        election_labels = ['2020 State', '2021 Town', '2021 Primary',
                          '2022 General', '2023 Town']
        election_counts = [
            sum(1 for v in voters if v.v20state),
            sum(1 for v in voters if v.v21town),
            sum(1 for v in voters if v.v21primary),
            sum(1 for v in voters if v.v22general),
            sum(1 for v in voters if v.v23town),
        ]
        
        fig3 = go.Bar(x=election_labels, y=election_counts)
        title_text3 = "Voter Participation in Elections"
        graph_div_elections = plotly.offline.plot(
            {"data": [fig3], "layout_title_text": title_text3},
            auto_open=False,
            output_type="div"
        )
        context['graph_div_elections'] = graph_div_elections
        
        return context
