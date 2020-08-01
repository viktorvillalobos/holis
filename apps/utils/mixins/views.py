class CompanyMixinViewSet:
    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company)
